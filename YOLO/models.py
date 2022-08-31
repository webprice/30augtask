from django.db import models
from django.contrib.auth.models import User

#

class Data(models.Model):
    title = models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    photo = models.CharField(max_length=200,null=True)
    seller = models.CharField(max_length=200,null=True)
