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
    context = {"auctions": Auction.objects.all()}

    return render_to_response(template, context, context_instance=RequestContext(request))


def search(request):
    if request.method == "POST" and "criteria" in request.POST:
        criteria = request.POST["criteria"]
        template = "home.html"
        context = {"auctions": Auction.objects.filter(Q(title__contains=criteria) | Q(description__contains=criteria))}

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
            message = "This is a confirmation message that you just created an auction with the title \""
            message += auction.title + "\"."
            send_mail("Auction created", message, "noreply@YAAS.com", [auction.seller.email], fail_silently=False)
            return HttpResponseRedirect("/YAAS/")

    template = "message.html"
    context = {"message": "Auction was not created"}
    # Auction was not created
    return render_to_response(template, context, context_instance=RequestContext(request))


def view_auction(request, id):
    auction = Auction.getById(id)
    if auction:
        template = "view_auction.html"
        context = {"auction": auction}
        return render_to_response(template, context, context_instance=RequestContext(request))
    else:
        template = "message.html"
        context = {"message": "Auction not found"}
        return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def edit_auction(request, id):
    auction = Auction.getById(id)
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
                    return HttpResponseRedirect("/YAAS/view_auction/" + str(auction.id) + "/")
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
        form = EditUserForm()
        if form.is_valid():
            # Save user and show message
            form.save()
            template = "message.html"
            context = {"message": "User info successfully updated."}
            return render_to_response(template, context, context_instance=RequestContext(request))
    else:
        # Empty user form
        form = EditUserForm({"email": user.email})
    template = "edit_user.html"
    context = {"user": user, "form": form}
    return render_to_response(template, context, context_instance=RequestContext(request))


def populate_database(request):
    Populate().doPopulate()
    return HttpResponseRedirect("/YAAS/")
