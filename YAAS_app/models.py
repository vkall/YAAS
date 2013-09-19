from django.db import models


class Auction(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    category = models.CharField(max_length=30)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()

    @classmethod
    def getById(cls, auction_id):
        return cls.objects.get(id=auction_id)
