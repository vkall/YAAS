"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from YAAS_app.models import *
from YAAS_app.forms import *


class MyBlogTest(TestCase):
    def setUp(self):
        self.username = "username"
        self.password = "password"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.createUrl = "/YAAS/auction/create/"
        self.confirmationUrl = "/YAAS/auction/create/confirmation/"

    def testAuthorizationCreateAuction(self):
        # If the client is not logged in, create_user should give a redirect status (302)
        response = self.client.get(self.createUrl)
        self.assertEqual(response.status_code, 302)

        # Login
        loggedIn = self.client.login(username=self.username, password=self.password)
        self.assertTrue(loggedIn)

        # If the client is logged in, editblog should give a success status (200)
        response = self.client.get(self.createUrl)
        self.assertEqual(response.status_code, 200)

    def testCreateAuction(self):
        auctionData= {
            "title": "title",
            "description": "description",
            "end_date": (timezone.now() + timedelta(days=4)).date(),
            "minimum_price": 10.50,
            "option": "Yes"
        }

        # Login
        loggedIn = self.client.login(username=self.username, password=self.password)
        self.assertTrue(loggedIn)

        # 0 auctions in database
        self.assertEqual(Auction.objects.all().count(), 0)

        # create auction by posting data
        self.client.post(self.confirmationUrl, auctionData)

        # 1 auction in database
        self.assertEqual(Auction.objects.all().count(), 1)
