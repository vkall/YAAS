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

    fixtures = ['test_fixture.json']

    def setUp(self):
        self.user1 = "user1"
        self.user2 = "user2"
        self.createUrl = "/YAAS/auction/create/"
        self.confirmationUrl = "/YAAS/auction/create/confirmation/"

    def testAuthorizationCreateAuction(self):
        # If the client is not logged in, create_user should give a redirect status (302)
        response = self.client.get(self.createUrl)
        self.assertEqual(response.status_code, 302)

        # Login
        loggedIn = self.client.login(username=self.user1, password=self.user1)
        self.assertTrue(loggedIn)

        # If the client is logged in, create_user should give a success status (200)
        response = self.client.get(self.createUrl)
        self.assertEqual(response.status_code, 200)

    def testCreateAuction(self):
        auctionData = {
            "title": "title",
            "description": "description",
            "end_date": (timezone.now() + timedelta(days=4)).date(),
            "minimum_price": 10.50,
            "option": "Yes"
        }

        # Login
        loggedIn = self.client.login(username=self.user1, password=self.user1)
        self.assertTrue(loggedIn)

        auctions = Auction.objects.all().count()
        # create auction by posting data
        self.client.post(self.confirmationUrl, auctionData)
        # auction count is 1 higher than before
        self.assertEqual(Auction.objects.all().count(), auctions+1)
