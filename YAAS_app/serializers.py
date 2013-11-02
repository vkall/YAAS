from rest_framework import serializers
from YAAS_app.models import *


class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = ('id','title', 'description', 'seller', 'start_date',
                  'updated_date', 'end_date', 'minimum_price', 'active', 'banned')