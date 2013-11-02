from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


class Auction(models.Model):
    id = models.AutoField(primary_key=True)
    seller = models.ForeignKey(User)
    title = models.CharField(max_length=30)
    description = models.TextField()
    start_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    end_date = models.DateTimeField()
    minimum_price = models.DecimalField(max_digits=16, decimal_places=2)
    active = models.BooleanField(default=True)
    banned = models.BooleanField(default=False)

    @classmethod
    def getActiveById(cls, auction_id):
        try:
            a = cls.objects.get(id=auction_id)
        except ObjectDoesNotExist:
            a = None
        if a and a.active and not a.banned:
            return a
        else:
            return None

    @classmethod
    def getActive(cls):
        return cls.objects.filter(Q(active=True) & Q(banned=False))

    @classmethod
    def findActive(cls, criteria):
        return cls.objects.filter((Q(title__contains=criteria) | Q(description__contains=criteria))
                                  & (Q(active=True) & Q(banned=False)))

    def getBidHistory(self):
        bids = Bid.getBidsForAuction(self)
        return bids

    def getLatestBid(self):
        bid = Bid.getLatestBidForAuction(self)
        if bid:
            return bid.bid
        else:
            return 0.00

    def getBidders(self):
        bids = self.getBidHistory()
        bidders = []
        for b in bids:
            if b.bidder not in bidders:
                bidders.append(b.bidder)

        return bidders


    def information(self):
        info = "ID: " + str(self.id) + "\n"
        info += "Title: " + self.title + "\n"
        info += "Description: " + self.description + "\n"
        info += "Started: " + str(self.start_date.date()) + "\n"
        info += "Updated: " + str(self.updated_date.date()) + "\n"
        info += "Ends: " + str(self.end_date.date()) + "\n"
        info += "Minimum price: " + str(self.minimum_price) + "\n"

        return info


class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    auction = models.ForeignKey(Auction)
    bidder = models.ForeignKey(User)
    bid = models.DecimalField(max_digits=16, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    @classmethod
    def getBidsForAuction(cls, auction):
        bids = cls.objects.filter(auction=auction).order_by("-timestamp")
        return bids

    @classmethod
    def getLatestBidForAuction(cls, auction):
        try:
            bid = cls.objects.filter(auction=auction).latest("timestamp")
        except ObjectDoesNotExist:
            bid = None
        return bid