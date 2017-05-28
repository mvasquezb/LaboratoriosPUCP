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


###Modelo de clientes


class Client(models.Model):
    name = models.CharField(max_length=100)
    idDoc = models.IntegerField()
    username = models.OneToOneField(User, on_delete=models.CASCADE)

# Modelo para pruebas
class SampleType(models.Model):
    description = models.CharField(max_length=100)
    active = models.BooleanField()


class Request(models.Model):
    description = models.CharField(max_length=100)
    client = models.ForeignKey(Client,on_delete=models.CASCADE)
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.description

class TestType(models.Model):
    description = models.CharField(max_length=100)
    active = models.BooleanField()


##Modelo para muestras

class SampleTemplate(models.Model):
    description = models.CharField(max_length=100)

    def __str__(self):
        return str(self.description)


class SampleFill(models.Model):
    requestFill = models.ForeignKey(Request,on_delete=models.CASCADE)
    sampleTemplate = models.ForeignKey(SampleTemplate)
    description = models.CharField(max_length=30)



##Modelo para pruebas


class EssayTemplate(models.Model):
    cod = models.IntegerField(default=0)
    test_n = models.IntegerField(default=0)
    description = models.CharField(max_length=100)

    def __str__(self):
        return str(self.cod)

    def getTest(self, index):
        array_test=TestTemplate.objects.filter(essayTemplate=self)
        return array_test[index-1]


class EssayFill(models.Model):
    essayTemplate = models.ForeignKey(EssayTemplate)
    description = models.CharField(max_length=100, default='essay testing')

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
    def create(self, essay_insert=None):
        if essay_insert is None:
            return
        self.essayTemplate = essay_insert
        test_n= self.essayTemplate.test_n
        self.save()
        for i in range(1,test_n+1):
            obj_test = TestFill()
            obj_test.create(self.essayTemplate.getTest(i), self)


class TestTemplate(models.Model):
    description = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    parameters_number = models.IntegerField(default=0)
    essayTemplate = models.ForeignKey(EssayTemplate)

    def __str__(self):
        return self.title

    def getParameter(self, index):
        array_par = ParameterTemplate.objects.filter(testTemplate=self)
        return array_par[index-1]


class TestFill(models.Model):

    # sampleFill = models.ForeignKey(SampleFill, on_delete=models.CASCADE)
    # requestFill = models.ForeignKey(Request,on_delete=models.CASCADE)
    testTemplate = models.ForeignKey(TestTemplate)
    essayFill = models.ForeignKey(EssayFill)
    description = models.CharField(max_length=100, default='descripcion')

    def __str__(self):
        return self.description


class LaboratoryType(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField()

    def create(self, test_insert=None, essay_insert=None):
        if test_insert is None:
            return
        if essay_insert is None:
            return
        self.essayFill = essay_insert
        self.testTemplate = test_insert
        self.description = 'Inserte descripcion aqui\n'
        par_n = self.testTemplate.parameters_number
        self.save()
        for i in range(1, par_n+1):
            obj_par = ParameterFill()
            obj_par.create(self, self.testTemplate.getParameter(i))
            obj_par.save()


class ParameterTemplate(models.Model):
    testTemplate = models.ForeignKey(TestTemplate)
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=100)
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


class ParameterFill(models.Model):
    parameterTemplate = models.ForeignKey(ParameterTemplate)
    testFill = models.ForeignKey(TestFill)
    value = models.CharField(max_length=100, default='Empty field')

    def __str__(self):
        return self.value + ' ' + self.parameterTemplate.__str__()

    def create(self, test_insert=None, para_insert=None):
        if para_insert is None:
            return
        if test_insert is None:
            return
        self.testFill = test_insert
        self.parameterTemplate = para_insert

