# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from YAAS_app.models import *
from YAAS_app.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def home(request):
    template = "home.html"
    context = {"auctions": Auction.objects.all()}

    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def create_auction(request):
    if request.method == "POST":
        form = CreateAuctionForm(request.POST)
        if form.is_valid():
            auction = Auction()
            auction.title = form.cleaned_data["title"]
            auction.seller = request.user
            auction.description = form.cleaned_data["description"]
            auction.end_date = form.cleaned_data["end_date"]
            auction.minimum_price = form.cleaned_data["minimum_price"]
            auction.save()
            return HttpResponseRedirect("/YAAS/")
    else:
        form = CreateAuctionForm()
    template = "create_auction.html"
    context = {"form": form}
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


def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Save user and redirect to front page
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

