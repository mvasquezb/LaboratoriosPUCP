from django.db import models

# Create your models here.


class Request(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Test(models.Model):
    name = models.CharField(max_length=100)
    request = models.ForeignKey(Request, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

