from django.db import models


class TypeLabs(models.Model):
    typename=models.CharField(max_length=100)
    active=models.BooleanField()

    def __str__(self):
        return "" + self.typename

class Labs(models.Model):
    labname=models.CharField(max_length=100)
    numUser=models.IntegerField()
    capacity=models.IntegerField()
    active=models.BooleanField(default=True)
    typeLab = models.ForeignKey(TypeLabs, on_delete=models.CASCADE)

### TipoEnsayo
class TypeAssay(models.Model):
    typename=models.CharField(max_length=100)
    active=models.BooleanField()

## Tipo Prueba
class TypeTest(models.Model):
    typename=models.CharField(max_length=100)
    active=models.BooleanField()

## Tipo Muestra
class TypeSample(models.Model):
    typename=models.CharField(max_length=100)
    active=models.BooleanField()
