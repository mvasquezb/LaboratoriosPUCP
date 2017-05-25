from django.db import models

# Create your models here.
class Labs(models.Model):
    labname=models.CharField(max_length=100)
    numUser=models.IntegerField()
    capacity=models.IntegerField()
    active=models.BooleanField()


class Labs(models.Model):
    labname=models.CharField(max_length=100)
    numUser=models.IntegerField()
    capacity=models.IntegerField()
    active=models.BooleanField()
