# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from YAAS_app.models import *
from YAAS_app.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


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
            auction.name = form.cleaned_data["title"]
            auction.category = form.cleaned_data["category"]
            auction.startDate = form.cleaned_data["start_date"]
            auction.endDate = form.cleaned_data["end_date"]
            auction.save()
            return HttpResponseRedirect("/YAAS/")
    else:
        form = CreateAuctionForm()
    template = "create_auction.html"
    context = {"form": form}
    return render_to_response(template, context, context_instance=RequestContext(request))


def view_auction(request, id):
    auctions = Auction.objects.filter(id=id)
    if len(auctions) > 0:
        template = "view_auction.html"
        context = {"auction": Auction.getById(id)}
        return render_to_response(template, context, context_instance=RequestContext(request))
    else:
        return HttpResponse("Auction not found")


def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Save user and redirect to front page
            form.save()
            return HttpResponseRedirect("/YAAS/")
    else:
        # Empty user form
        form = UserRegistrationForm()
    template = "register_user.html"
    context = {"form": form}
    return render_to_response(template, context, context_instance=RequestContext(request))

