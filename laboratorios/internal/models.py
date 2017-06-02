from django.db import models
from django.contrib.auth.models import User as AuthUser


# MODELO DE PRUEBA, NO SE RELACIONA
class Test (models.Model):
    name = models.CharField (max_length=100)
    request = models.ForeignKey ("Request", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Access (models.Model):
    description = models.CharField (max_length=100)

    def __str__(self):
        return self.description


# Modelo para usuarios
class Role (models.Model):
    description = models.CharField (max_length=100, blank=True)
    access = models.ManyToManyField (Access, through="RoleByAccess")

    def __str__(self):
        return self.description


class RoleByAccess (models.Model):
    role = models.ForeignKey (Role)
    access = models.ForeignKey (Access)


class User (AuthUser):
    role = models.ManyToManyField (Role, through="UserByRole")

    def __str__(self):
        return self.get_full_name () or self.username


class UserByRole (models.Model):
    user = models.ForeignKey (User)
    role = models.ForeignKey (Role)

    def __str__(self):
        return "{} | {}".format (self.user, self.role)


# Modelo de clientes
class Client (models.Model):
    name = models.CharField (max_length=100)
    idDoc = models.IntegerField ()
    username = models.OneToOneField (User, on_delete=models.CASCADE)


# Model de tipo de laboratorio
class LaboratoryType (models.Model):
    name = models.CharField (max_length=100)
    description = models.CharField (max_length=200, blank=True)
    active = models.BooleanField ()

    def __str__(self):
        return self.name


### TipoEnsayo
class EssayType (models.Model):
    name = models.CharField (max_length=100)
    description = models.CharField (max_length=100)
    active = models.BooleanField ()
    lab_type = models.ForeignKey (LaboratoryType,null=True, on_delete=models.CASCADE)


class TestType (models.Model):
    name = models.CharField (max_length=100)
    description = models.CharField (max_length=100)
    active = models.BooleanField ()
    essay_type = models.ForeignKey (EssayType, on_delete=models.CASCADE)


class Request (models.Model):
    description = models.CharField (max_length=100)
    client = models.ForeignKey (Client, on_delete=models.CASCADE)
    status = models.IntegerField (default=0)


# Modelo para muestras
class SampleTemplate (models.Model):
    description = models.CharField (max_length=100)

    def __str__(self):
        return str (self.description)


class SampleFill (models.Model):
    request_fill = models.ForeignKey (Request, on_delete=models.CASCADE)
    sample_template = models.ForeignKey (SampleTemplate)
    description = models.CharField (max_length=30)


# Modelo para pruebas
class EssayTemplate (models.Model):
    code = models.IntegerField (default=0)
    test_number = models.IntegerField (default=0)
    description = models.CharField (max_length=100)

    def __str__(self):
        return str (self.cod)

    def get_test(self, index):
        test_list = TestTemplate.objects.filter (essay_template=self)
        return test_list[index - 1]


class EssayFill (models.Model):
    essay_template = models.ForeignKey (EssayTemplate)
    description = models.CharField (max_length=100, default='essay testing')

    def __str__(self):
        return self.description

    def create(self, essay_insert=None):
        if essay_insert is None:
            return
        self.essay_template = essay_insert
        test_number = self.essay_template.test_number
        self.save ()
        for i in range (1, test_number + 1):
            obj_test = TestFill ()
            obj_test.create (self.essay_template.get_test (i), self)


class TestTemplate (models.Model):
    description = models.CharField (max_length=100)
    title = models.CharField (max_length=100)
    parameters_number = models.IntegerField (default=0)
    essay_template = models.ForeignKey (EssayTemplate)

    def __str__(self):
        return self.title

    def get_parameter(self, index):
        parameter_list = ParameterTemplate.objects.filter (test_template=self)
        return parameter_list[index - 1]


class TestFill (models.Model):
    # sampleFill = models.ForeignKey(SampleFill, on_delete=models.CASCADE)
    # requestFill = models.ForeignKey(Request,on_delete=models.CASCADE)
    test_template = models.ForeignKey (TestTemplate)
    essay_fill = models.ForeignKey (EssayFill)
    description = models.CharField (max_length=100, default='descripcion')

    def __str__(self):
        return self.description

    def create(self, test_insert=None, essay_insert=None):
        if test_insert is None:
            return
        if essay_insert is None:
            return
        self.essay_fill = essay_insert
        self.test_template = test_insert
        self.description = 'Inserte descripcion aqui\n'
        par_n = self.test_template.parameters_number
        self.save ()
        for i in range (1, par_n + 1):
            obj_par = ParameterFill ()
            obj_par.create (self, self.test_template.get_parameter (i))
            obj_par.save ()


class ParameterTemplate (models.Model):
    test_template = models.ForeignKey (TestTemplate)
    name = models.CharField (max_length=100)
    unit = models.CharField (max_length=100)

    def __str__(self):
        return self.name


class ParameterFill (models.Model):
    parameter_template = models.ForeignKey (ParameterTemplate)
    test_fill = models.ForeignKey (TestFill)
    value = models.CharField (max_length=100, default='Empty field')

    def __str__(self):
        return self.value + ' | ' + str (self.parameter_template)

    def create(self, test_insert=None, param_insert=None):
        if param_insert is None or test_insert is None:
            return
        self.test_fill = test_insert
        self.parameter_template = param_insert


class Laboratory (models.Model):
    name = models.CharField (max_length=100)
    users_number = models.IntegerField ()
    capacity = models.IntegerField ()
    active = models.BooleanField ()
    type = models.ForeignKey (LaboratoryType, on_delete=models.CASCADE)


## Tipo Muestra
class SampleType (models.Model):
    name = models.CharField (max_length=100)
    description = models.CharField (max_length=100)
    active = models.BooleanField ()
    lab_type = models.ForeignKey (LaboratoryType, null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
