from django.db import models

# Create your models here.


class Client(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Sale(models.Model):
    ammount = models.FloatField()

    def __str__(self):
        return "Monto venta " + str(self.pk) + ": " + str(self.ammount)


class Product(models.Model):
    description = models.CharField(max_length=100)
    unit_cost = models.FloatField()
