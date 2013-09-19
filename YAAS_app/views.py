# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from YAAS_app.models import *


def home(request):

    template = "home.html"
    context = {"auctions": Auction.objects.all()}

    return render_to_response(template, context)


def create_auction(request):
    auction = Auction()

    if request.method == "POST" and "name" in request.POST:
        auction.name = request.POST["name"]
        auction.category = request.POST["category"]
        auction.startDate = request.POST["startDate"]
        auction.endDate = request.POST["endDate"]
        auction.save()

        return HttpResponseRedirect('/YAAS/')
    else:
        template = "create_auction.html"
        return render_to_response(template, context_instance=RequestContext(request))
