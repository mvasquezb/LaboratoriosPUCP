from django.db import models


class Test(models.Model):
    name = models.CharField(max_length=100)
    request = models.ForeignKey("Request", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Access(models.Model):
    description = models.CharField(max_length=100)
    def __str__(self):
        return self.description


# Modelo para usuarios
class Role(models.Model):
    description = models.CharField(max_length=100, blank=True)
    access = models.ManyToManyField(Access, through="RoleByAccess")
    def __str__(self):
        return self.description


class RoleByAccess(models.Model):
    role = models.ForeignKey(Role)
    access = models.ForeignKey(Access)


class User(models.Model):
    username = models.CharField(max_length=100, null=False)
    userDescription = models.CharField(max_length=200, null=True)
    password = models.CharField(max_length=20)
    role = models.ManyToManyField(Role, through="UserByRole")

    def __str__(self):
        return "%s %s" % (self.username, self.userDescription)


class UserByRole(models.Model):
    user = models.ForeignKey(User)
    role = models.ForeignKey(Role)

    def __str__(self):
        return "%s %s" % (self.user, self.role)
# Modelo de clientes
class Client(models.Model):
    name = models.CharField(max_length=100)
    idDoc = models.IntegerField()
    username = models.OneToOneField(User, on_delete=models.CASCADE)
# Modelo para pruebas
class SampleType(models.Model):
    description = models.CharField(max_length=100)
    active = models.BooleanField()

    def __str__(self):
        return self.description


class TestType(models.Model):
    description = models.CharField(max_length=100)
    active = models.BooleanField()


class Request(models.Model):
    description = models.CharField(max_length=100)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.description


class Sample(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    sampleType = models.ForeignKey(SampleType)
    description = models.CharField(max_length=30)


class TestFill(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    testType = models.ForeignKey(TestType)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description


class LaboratoryType(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField()

    def __str__(self):
        return self.name


class Laboratory(models.Model):
    name = models.CharField(max_length=100)
    users_number = models.IntegerField()
    capacity = models.IntegerField()
    active = models.BooleanField()
    type = models.ForeignKey(LaboratoryType, on_delete=models.CASCADE)


# TipoEnsayo
class EssayType(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField()
