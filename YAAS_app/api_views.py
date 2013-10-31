from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Q
from YAAS_app.models import *
from YAAS_app.serializers import *


@api_view(['GET'])
def api_list_auctions(request, format=None):
    # List all blog posts or create a new blog post

    if request.method == 'GET':
        auctions = Auction.objects.all()
        serializer = AuctionSerializer(auctions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def api_search_auctions(request, criteria, format=None):
    # List all blog posts or create a new blog post

    if request.method == 'GET':
        auctions = Auction.objects.filter(Q(title__contains=criteria) | Q(description__contains=criteria))
        serializer = AuctionSerializer(auctions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
