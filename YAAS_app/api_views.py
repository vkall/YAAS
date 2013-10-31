from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from YAAS_app.models import *
from YAAS_app.serializers import *


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
def api_auctions(request, format=None):
    # List all blog posts or create a new blog post

    if request.method == 'GET':
        auctions = Auction.objects.all()
        serializer = AuctionSerializer(auctions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


