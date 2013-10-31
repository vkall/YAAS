from rest_framework import serializers
from YAAS_app.models import *


class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = ('title', 'description', 'end_date', 'minimum_price')