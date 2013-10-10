from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class Auction(models.Model):
    id = models.AutoField(primary_key=True)
    seller = models.ForeignKey(User, related_name='seller')
    title = models.CharField(max_length=30)
    description = models.TextField()
    start_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    end_date = models.DateTimeField()
    minimum_price = models.DecimalField(max_digits=16, decimal_places=2)
    current_bid = models.DecimalField(max_digits=16, decimal_places=2, null=True)
    bidder = models.ForeignKey(User, related_name='bidder', null=True)

    @classmethod
    def getById(cls, auction_id):
        try:
            a = cls.objects.get(id=auction_id)
        except ObjectDoesNotExist:
            a = None
        return a
