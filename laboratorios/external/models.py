from django.db import models

# Create your models here.
class ExternalClient(models.Model):
    name = models.CharField(max_length=200)
    contract_detail = models.CharField(max_length=200)


