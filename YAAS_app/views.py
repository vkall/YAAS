# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from YAAS_app.models import *


def home(request):
    template = "home.html"
    context = {"auctions": Auction.objects.all()}

    return render_to_response(template, context)


def create_auction(request):
    if request.method == "POST" and all(val in request.POST for val in ["name", "category", "startDate", "endDate"]):
        auction = Auction()
        auction.name = request.POST["name"]
        auction.category = request.POST["category"]
        auction.startDate = request.POST["startDate"]
        auction.endDate = request.POST["endDate"]
        auction.save()
        return HttpResponseRedirect("/YAAS/")
    else:
        template = "create_auction.html"
        return render_to_response(template, context_instance=RequestContext(request))


def view_auction(request, id):
    auctions = Auction.objects.filter(id=id)
    if len(auctions) > 0:
        template = "view_auction.html"
        context = {"auction": Auction.getById(id)}
        return render_to_response(template, context)
    else:
        return HttpResponse("Auction not found")