from django.db import models

# Create your models here.


### Clase de las solicitudes
class RequestStorage(models.Model):
    numEnsayo = models.IntegerField()
    muestra = models.CharField(max_length=100)
    tipoMuestra = models.CharField(max_length=100)
    cliente = models.CharField(max_length=100)
    pendiente = models.BooleanField()
    aprobado = models.BooleanField()
