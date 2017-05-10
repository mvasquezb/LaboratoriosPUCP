from django.db import models

# Create your models here.


class Client(models.Model):
	name = models.CharField(max_length=100)


class Sale(models.Model):
	ammount = models.FloatField()


class Product(models.Model):
	description = models.CharField(max_length=100)
	unit_cost = models.FloatField()

	