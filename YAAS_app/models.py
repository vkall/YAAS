from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


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
    def getById(cls, auction_id):
        try:
            a = cls.objects.get(id=auction_id)
        except ObjectDoesNotExist:
            a = None
        return a


class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    auction = models.ForeignKey(Auction)
    bidder = models.ForeignKey(User)
    bid = models.DecimalField(max_digits=16, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
