from django.db import models
from django.contrib.auth.models import (
    User as AuthUser,
    Permission
)


class Role(models.Model):
    permissions = models.ManyToManyField(Permission)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)


class BasicUser(AuthUser):
    roles = models.ManyToManyField(Role)

    def __str__(self):
        return self.get_full_name() or self.username


class Client(BasicUser):
    code = models.CharField(max_length=10)
    doc_number = models.IntegerField()
    phone_number = models.CharField(max_length=20)


class Employee(BasicUser):
    essay_methods = models.ManyToManyField(
        'EssayMethod',
        related_name='employees'
    )
    assigned_essay_methods = models.ManyToManyField(
        'EssayMethodFill',
        related_name='employees'
    )


class LaboratoryServiceHours(models.Model):
    start_time = models.PositiveIntegerField()
    end_time = models.PositiveIntegerField()

    def __str__(self):
        return str(self.start_time) + ' - ' + str(self.end_time)


class Laboratory(models.Model):
    name = models.CharField(max_length=50)
    employees = models.ManyToManyField('Employee', related_name='laboratories')
    capacity = models.PositiveIntegerField()
    supervisor = models.ForeignKey('Employee')
    service_hours = models.ForeignKey(LaboratoryServiceHours)
    essay_methods = models.ManyToManyField(
        'EssayMethod',
        related_name='laboratories'
    )
    inventory = models.ManyToManyField(
        'Inventory',
        related_name='laboratories'
    )


class Essay(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    essay_methods = models.ManyToManyField(
        'EssayMethod',
        related_name='essays'
    )

    def get_essay_methods(self):
        return EssayMethod.objects.filter(essays=self)

    def get_essay_methods_count(self):
        return len(self.get_essay_methods())

    def get_essay_method(self, index):
        if (index>0 and index<=self.get_essay_methods_count()):
            return self.get_essay_methods()[index-1]
   


class EssayMethod(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    price = models.FloatField()
    parameters = models.ManyToManyField(
        'EssayMethodParameter',
        related_name='essaymethods'
    )

    def __str__(self):
        return self.name
    
    def get_parameters(self):
        return EssayMethodParameter.objects.filter(essaymethods=self)

    def get_parameter_count(self):
        return len(self.get_parameters())

    def get_parameter(self,index):
        if (i>0 and i<=self.get_parameter_count()):
            return self.get_parameters()[i]


class EssayMethodParameter(models.Model):
    description = models.CharField(max_length=100)
    unit = models.CharField(max_length=20)

    def __str__(self):
        return self.description + ' | ' + self.unit




class EssayFill(models.Model):
    essay = models.ForeignKey(Essay)
    sample = models.ForeignKey('Sample')

    def __str__(self):
        return self.essay.name

    def create(self, essay_insert=None):    # function for creating essay tree
        if essay_insert is None:
            return
        self.essay = essay_insert
        self.save()
        test_number = self.essay.get_essay_methods_count()
        for i in range(1, test_number+1):
            obj_test = EssayMethodFill()
            obj_test.create(self.essay.get_essay_method(i),self)
            obj_test.save()



class EssayMethodFill(models.Model):
    essay_method = models.ForeignKey(EssayMethod)
    essay = models.ForeignKey(EssayFill)
    external_provider = models.ForeignKey('ExternalProvider', null=True)
    inventory_order = models.ForeignKey('InventoryOrder', null=True)
    chosen = models.BooleanField(default=False)

    def __str__(self):
        return essay_method.name
    
    def create(self, essay_method_insert = None, essay_insert = None):
        if essay_method_insert is None or essay_insert is None:
            return
        self.essay_method = essay_method_insert
        self.essay = essay_insert
        self.save()
        parameters_number = essay_method_insert.get_parameter_count()
        for i in range(1,parameters_number+1):
            obj_par = EssayMethodParameterFill()
            obj_par.create(self, self.essay_method.get_parameter(i))
            obj_par.save()


class EssayMethodParameterFill(models.Model):
    parameter = models.ForeignKey(EssayMethodParameter)
    value = models.CharField(max_length=20)  # Is this always a numeric value ?
    uncertainty = models.FloatField()
    essay_method = models.ForeignKey(EssayMethodFill)

    def __str__(self):
        return str(self.parameter) + ' | ' + self.value

    def create(self, essay_method_insert = None, essay_method_parameter_insert = None):
        if (essay_method_insert is None or essay_method_parameter_insert is None):
            return
        self.essay_method = essay_method_insert
        self.parameter = essay_method_parameter_insert
        self.save()


class ExternalProvider(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    services = models.ManyToManyField('ExternalProviderService')


class ExternalProviderService(models.Model):
    description = models.CharField(max_length=500)


class ServiceRequest(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Employee)
    state = models.ForeignKey('ServiceRequestState')
    observations = models.CharField(max_length=500)


class ServiceRequestState(models.Model):
    slug = models.CharField(max_length=20)
    description = models.CharField(max_length=20)

    def __str__(self):
        return self.description


class RequestAttachment(models.Model):
    request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    # file = models.FileField()  # Should we save the file in DB or in server, or at all ?


class ServiceContract(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)


class ServiceContractModification(models.Model):
    contract = models.ForeignKey(ServiceContract, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)


# Cotización
class Quotation(models.Model):
    request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)


class SampleType(models.Model):
    slug = models.CharField(max_length=50)
    name = models.CharField(max_length=100)


class Sample(models.Model):
    name = models.CharField(max_length=50, default='Insertar nombre de muestra')
    code = models.CharField(max_length=10,default='#######')
    sample_type = models.ForeignKey(SampleType)
    request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    inventory = models.ForeignKey('Inventory', on_delete=models.CASCADE)
    


class Inventory(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)


class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    location = models.CharField(max_length=200)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)


class InventoryOrder(models.Model):
    essay = models.ForeignKey(EssayFill)


class InventoryOrderDefault(models.Model):
    detail = models.CharField(max_length=100)
