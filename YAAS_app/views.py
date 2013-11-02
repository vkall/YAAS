# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.db.models import Q
from YAAS_app.models import *
from YAAS_app.forms import *
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from fixtures import *


def home(request):
    template = "home.html"
    context = {"auctions": Auction.getActive()}

    return render_to_response(template, context, context_instance=RequestContext(request))


def search(request):
    if request.method == "POST" and "criteria" in request.POST:
        criteria = request.POST["criteria"]
        template = "home.html"
        context = {"auctions": Auction.findActive(criteria)}

        return render_to_response(template, context, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/YAAS/")


@login_required
def create_auction(request):
    if request.method == "POST":
        form = CreateAuctionForm(request.POST)
        if form.is_valid():
            template = "confirmation.html"
            context = {"form": ConfirmationForm(), "auctionform": form}
            # Valid auction form, redirect to confirmation page
            return render_to_response(template, context, context_instance=RequestContext(request))
    else:
        form = CreateAuctionForm()
    template = "create_auction.html"
    context = {"form": form}
    return render_to_response(template, context, context_instance=RequestContext(request))


def confirmation(request):
    option = request.POST.get('option', '')
    if option == 'Yes':
        # Confirmation was 'Yes', save auction, send email and redirect to front page.
        form = CreateAuctionForm(request.POST)
        if form.is_valid():
            auction = Auction()
            auction.title = form.cleaned_data["title"]
            auction.seller = request.user
            auction.description = form.cleaned_data["description"]
            auction.end_date = form.cleaned_data["end_date"]
            auction.minimum_price = form.cleaned_data["minimum_price"]
            auction.save()
            message = "This is a confirmation message that the following auction has been created: \n\n"
            message += auction.information()
            send_mail("Auction created", message, "noreply@YAAS.com", [auction.seller.email], fail_silently=False)
            return HttpResponseRedirect("/YAAS/")

    template = "message.html"
    context = {"message": "Auction was not created"}
    # Auction was not created
    return render_to_response(template, context, context_instance=RequestContext(request))


def view_auction(request, id):
    auction = Auction.getActiveById(id)
    if auction:
        template = "view_auction.html"
        context = {"auction": auction, "bid_history": auction.getBidHistory(), "bid_form": BidForm()}
        return render_to_response(template, context, context_instance=RequestContext(request))
    else:
        template = "message.html"
        context = {"message": "Auction not found"}
        return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def edit_auction(request, id):
    auction = Auction.getActiveById(id)
    if auction:
        if request.user.id != auction.seller.id:
            template = "message.html"
            context = {"message": "Only the seller of an auction can edit it!"}
            # Error: Logged in user is not the same as the seller!
            return render_to_response(template, context, context_instance=RequestContext(request))
        else:
            if request.method == "POST":
                form = EditAuctionForm(request.POST)
                if form.is_valid():
                    auction.description = form.cleaned_data["description"]
                    auction.save()
                    # If logged in user is the same as the seller and request is POST, save edits
                    return HttpResponseRedirect("/YAAS/auction/" + str(auction.id) + "/")
            else:
                form = EditAuctionForm({"description": auction.description})
            template = "edit_auction.html"
            context = {"form": form, "auction": auction}
            # If logged in user is the same as the seller and request is not POST, view edit form
            return render_to_response(template, context, context_instance=RequestContext(request))
    else:
        template = "message.html"
        context = {"message": "Auction not found"}
        # Error: Auction not found!
        return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def ban_auction(request, id):
    auction = Auction.getActiveById(id)
    template = "message.html"
    if auction:
        if request.user.is_superuser:
            auction.banned = True
            auction.save()

            # Auction banned, send email to seller and bidders
            receivers = [auction.seller.email, ]
            bidders = auction.getBidders()
            for b in bidders:
                receivers.append(b.email)
            message = "The following auction has been banned: \n\n"
            message += auction.information()
            send_mail("Auction banned", message, "noreply@YAAS.com", receivers, fail_silently=False)

            context = {"message": "Auction number " + str(auction.id) + " was banned!"}
            return render_to_response(template, context, context_instance=RequestContext(request))
        else:
            context = {"message": "Must be admin to ban auction!"}
            # Error: Logged in user is not an admin!
            return render_to_response(template, context, context_instance=RequestContext(request))
    else:
        context = {"message": "Auction not found"}
        # Error: Auction not found!
        return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def bid_auction(request, id):
    auction = Auction.getActiveById(id)
    if auction:
        latest_bid = Bid.getLatestBidForAuction(auction)
        if request.user.id == auction.seller.id:
            template = "message.html"
            context = {"message": "You can't bid on your own auctions!"}
            # Error: Seller tried to bid on own auction
            return render_to_response(template, context, context_instance=RequestContext(request))
        elif request.user.id == latest_bid.bidder.id:
            template = "message.html"
            context = {"message": "You can't bid on an auction that you are already winning!"}
            # Error: Winning bidder tried to bid again
            return render_to_response(template, context, context_instance=RequestContext(request))
        else:
            if request.method == "POST":
                form = BidForm(request.POST)
                if (form.is_valid() and form.cleaned_data["bid"] > auction.minimum_price
                        and form.cleaned_data["bid"] > latest_bid.bid):
                    # Create a bid
                    bid = Bid()
                    bid.bid = form.cleaned_data["bid"]
                    bid.auction = auction
                    bid.bidder = request.user
                    bid.save()

                    # Notify bidder, last bidder and seller by email
                    receivers = [request.user.email, latest_bid.bidder.email, auction.seller.email]
                    message = request.user.get_full_name() + " made a bid on the following auction: \n\n"
                    message += auction.information()
                    message += "\n\nThe new bid is " + str(bid.bid)
                    send_mail("New bid on auction", message, "noreply@YAAS.com", receivers, fail_silently=False)

                    return HttpResponseRedirect("/YAAS/auction/" + str(auction.id) + "/")
            else:
                form = BidForm()
            template = "view_auction.html"
            context = {"auction": auction, "bid_history": auction.getBidHistory(), "bid_form": form}
            return render_to_response(template, context, context_instance=RequestContext(request))
    else:
        template = "message.html"
        context = {"message": "Auction not found"}
        # Error: Auction not found!
        return render_to_response(template, context, context_instance=RequestContext(request))


def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Save user and show message
            form.save()
            template = "message.html"
            context = {"message": "User successfully created, please login."}
            return render_to_response(template, context, context_instance=RequestContext(request))
    else:
        # Empty user form
        form = UserRegistrationForm()
    template = "register_user.html"
    context = {"form": form}
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def edit_user(request):
    user = request.user
    if request.method == "POST":
        form = EditUserForm(request.POST)
        if form.is_valid():
            # Save user and show message
            user.email = form.cleaned_data["email"]
            user.set_password(form.cleaned_data["password"])
            user.save()
            template = "message.html"
            context = {"message": "User info successfully updated."}
            return render_to_response(template, context, context_instance=RequestContext(request))
    else:
        form = EditUserForm({"email": user.email})
    template = "edit_user.html"
    context = {"user": user, "form": form}
    return render_to_response(template, context, context_instance=RequestContext(request))


def populate_database(request):
    Populate().doPopulate()
    return HttpResponseRedirect("/YAAS/")