from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
from random import randint

from YAAS_app.models import *


class Populate:

    def addUser(self, number):
        user = User()
        user.username = "user" + str(number)
        user.set_password("user" + str(number))
        user.first_name = "First" + str(number)
        user.last_name = "Last" + str(number)
        user.email = "user" + str(number) + "@yaasmail.com"
        user.save()

    def addAuction(self, number):
        auction = Auction()
        auction.title = "Title" + str(number)
        auction.description = "This is a description of item number " + str(number)
        auction.minimum_price = 24.50 + number
        auction.end_date = timezone.now() + timedelta(days=randint(3, 7))
        auction.seller = User.objects.get(username="user"+str(randint(1,50)))
        auction.save()

    def doPopulate(self):

        # Create admin
        User.objects.create_superuser(username="admin", password="admin", email="admin@yaasmail.com")

        # Create 50 users
        for number in range(1, 51):
            self.addUser(number)

        # Create 50 auctions with random sellers
        for number in range(1, 51):
            self.addAuction(number)