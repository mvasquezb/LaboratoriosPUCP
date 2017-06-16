from django.db import models
from django.contrib.auth.models import (
    User as AuthUser,
    Permission
)
from django.forms.widgets import HiddenInput

from safedelete.models import (
    SOFT_DELETE_CASCADE,
    SafeDeleteModel
)
from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField


@auditlog.register()
class Role(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    audit_log = AuditlogHistoryField()
    permissions = models.ManyToManyField(Permission, blank=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    registered_date = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        blank=True,
    )


@auditlog.register()
class BasicUser(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    audit_log = AuditlogHistoryField()
    user = models.OneToOneField(AuthUser, on_delete=models.PROTECT)
    roles = models.ManyToManyField(Role)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


@auditlog.register()
class Client(BasicUser):
    _safedelete_policy = SOFT_DELETE_CASCADE

    # audit_log = AuditlogHistoryField()
    code = models.CharField(max_length=10)
    doc_number = models.IntegerField()
    phone_number = models.CharField(max_length=20)
    registered_date = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        blank=True
    )


@auditlog.register()
class Employee(BasicUser):
    _safedelete_policy = SOFT_DELETE_CASCADE

    # audit_log = AuditlogHistoryField()
    essay_methods = models.ManyToManyField(
        'EssayMethod',
        related_name='employees',
        blank=True
    )
    assigned_essay_methods = models.ManyToManyField(
        'EssayMethodFill',
        related_name='employees',
        blank=True
    )
    registered_date = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        blank=True
    )


@auditlog.register()
class LaboratoryServiceHours(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    audit_log = AuditlogHistoryField()
    start_time = models.PositiveIntegerField()
    end_time = models.PositiveIntegerField()
    registered_date = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        blank=True
    )

    def __str__(self):
        return str(self.start_time) + ' - ' + str(self.end_time)


@auditlog.register()
class Laboratory(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    audit_log = AuditlogHistoryField()
    name = models.CharField(max_length=50, unique=True)
    employees = models.ManyToManyField(
        'Employee',
        related_name='laboratories',
        blank=True
    )
    capacity = models.PositiveIntegerField()
    supervisor = models.ForeignKey('Employee', null=True, blank=True)
    service_hours = models.ForeignKey(LaboratoryServiceHours)
    essay_methods = models.ManyToManyField(
        'EssayMethod',
        related_name='laboratories',
        blank=True
    )
    inventory = models.ManyToManyField(
        'Inventory',
        related_name='laboratories',
        blank=True
    )
    registered_date = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        blank=True
    )


@auditlog.register()
class Essay(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    audit_log = AuditlogHistoryField()
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    registered_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    essay_methods = models.ManyToManyField(
        'EssayMethod',
        related_name='essays',
        blank=True
    )
    registered_date = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        blank=True
    )

    def __str__(self):
        return self.name

    def get_essay_methods(self):
        return EssayMethod.all_objects.filter(
            deleted__isnull=True,
            essays=self
        )

    def get_essay_methods_count(self):
        return len(self.get_essay_methods())

    def get_essay_method(self, index):
        if (index > 0 and index <= self.get_essay_methods_count()):
            return self.get_essay_methods()[index - 1]


@auditlog.register()
class EssayMethod(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    audit_log = AuditlogHistoryField()
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    price = models.FloatField()
    parameters = models.ManyToManyField(
        'EssayMethodParameter',
        related_name='essaymethods',
        blank=True
    )
    sample_types = models.ManyToManyField(
        'SampleType',
        related_name='essay_methods',
        blank=True
    )
    registered_date = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        blank=True
    )

    def __str__(self):
        return self.name

    def get_parameters(self):
        return EssayMethodParameter.all_objects.filter(
            deleted__isnull=True,
            essaymethods=self
        )

    def get_parameter_count(self):
        return len(self.get_parameters())

    def get_parameter(self, index):
        if index > 0 and index <= self.get_parameter_count():
            return self.get_parameters()[index - 1]


@auditlog.register()
class EssayMethodParameter(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    audit_log = AuditlogHistoryField()
    description = models.CharField(max_length=100)
    unit = models.CharField(max_length=20)
    registered_date = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        blank=True
    )

    def __str__(self):
        return self.description + ' | ' + self.unit


@auditlog.register()
class EssayFill(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    audit_log = AuditlogHistoryField()
    essay = models.ForeignKey(Essay)
    sample = models.ForeignKey('Sample')
    quantity = models.PositiveIntegerField(default=0)
    quotation = models.ForeignKey(
        'Quotation',
        related_name='essay_fills',
        null=True,
        blank=True
    )
    registered_date = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        blank=True
    )

    def __str__(self):
        return self.essay.name

    def create(self, essay_insert=None):    # function for creating essay tree
        if essay_insert is None:
            return
        self.essay = essay_insert
        self.save()
        test_number = self.essay.get_essay_methods_count()
        for i in range(1, test_number + 1):
            obj_test = EssayMethodFill()
            obj_test.create(self.essay.get_essay_method(i), self)
            obj_test.save()

    # function for destroying old tree and creating new one
    def recreate(self, essay_insert=None):
        if essay_insert is None:
            return

        methods_to_delete = EssayMethodFill.objects.filter(
            deleted__isnull=True,
            essay=self
        )
        for i in range(0, len(methods_to_delete)):
            methods_to_delete[i].delete()

        self.essay = essay_insert
        self.save()
        test_number = self.essay.get_essay_methods_count()
        for i in range(1, test_number + 1):
            obj_test = EssayMethodFill()
            obj_test.create(self.essay.get_essay_method(i), self)
            obj_test.save()


@auditlog.register()
class EssayMethodFill(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    audit_log = AuditlogHistoryField()
    essay_method = models.ForeignKey(
        EssayMethod,
        on_delete=models.CASCADE,
        related_name='essay_methods'
    )
    essay = models.ForeignKey(EssayFill)
    external_provider = models.ForeignKey(
        'ExternalProvider',
        null=True,
        blank=True
    )
    inventory_order = models.ForeignKey(
        'InventoryOrder',
        null=True,
        blank=True
    )
    chosen = models.BooleanField(default=False)
    registered_date = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        blank=True
    )

    def __str__(self):
        return self.essay_method.name

    def create(self, essay_method_insert=None, essay_insert=None):
        if essay_method_insert is None or essay_insert is None:
            return
        self.essay_method = essay_method_insert
        self.essay = essay_insert
        self.save()
        parameters_number = essay_method_insert.get_parameter_count()
        for i in range(1, parameters_number + 1):
            obj_par = EssayMethodParameterFill()
            obj_par.create(self, self.essay_method.get_parameter(i))
            obj_par.save()


@auditlog.register()
class EssayMethodParameterFill(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    audit_log = AuditlogHistoryField()
    parameter = models.ForeignKey(EssayMethodParameter)
    value = models.CharField(
        max_length=20,
        default='',
        blank=True
    )  # Is this always a numeric value ?
    uncertainty = models.FloatField(default=0, blank=True)
    essay_method = models.ForeignKey(
        EssayMethodFill,
        on_delete=models.CASCADE,
        related_name='parameters'
    )
    registered_date = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        blank=True
    )

    def __str__(self):
        return str(self.parameter) + ' | ' + self.value or ''

    def create(self,
               essay_method_insert=None,
               essay_method_param_insert=None):
        if essay_method_insert is None or essay_method_param_insert is None:
            return
        self.essay_method = essay_method_insert
        self.parameter = essay_method_param_insert
        print(self)
        self.save()


@auditlog.register()
class ExternalProvider(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    audit_log = AuditlogHistoryField()
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    services = models.ManyToManyField('ExternalProviderService', blank=True)
    registered_date = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        blank=True
    )

    def __str__(self):
        return self.name


@auditlog.register()
class ExternalProviderService(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    audit_log = AuditlogHistoryField()
    description = models.CharField(max_length=500)
    registered_date = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        blank=True
    )

    def __str__(self):
        return self.description


@auditlog.register()
class ServiceRequest(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    audit_log = AuditlogHistoryField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Employee)
    state = models.ForeignKey('ServiceRequestState')
    observations = models.CharField(max_length=500, null=True, blank=True)
    expected_duration = models.IntegerField(default=10)
    registered_date = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        blank=True
    )

    def __str__(self):
        return str(self.client) + ' | ' + str(self.state)


@auditlog.register()
class ServiceRequestState(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    audit_log = AuditlogHistoryField()
    slug = models.CharField(max_length=20)
    description = models.CharField(max_length=20)
    registered_date = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        blank=True
    )

    def __str__(self):
        return self.description


# Para el archivo adjunto
def content_file_name(instance, filename):
    return '/'.join(['requestFiles', str(instance.request.pk), filename])


@auditlog.register()
class RequestAttachment(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    audit_log = AuditlogHistoryField()
    request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    description = models.CharField(max_length=100, null=True, blank=True)
    fileName = models.CharField(max_length=100, null=True)
    file = models.FileField(upload_to=content_file_name, null=True, blank=True)
    registered_date = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        blank=True
    )

@auditlog.register()
class ServiceContract(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    audit_log = AuditlogHistoryField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    registered_date = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        blank=True
    )

@auditlog.register()
class ServiceContractModification(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    audit_log = AuditlogHistoryField()
    contract = models.ForeignKey(ServiceContract, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    registered_date = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        blank=True
    )


# Cotización
@auditlog.register()
class Quotation(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    audit_log = AuditlogHistoryField()
    request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    registered_date = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        blank=True
    )

@auditlog.register()
class SampleType(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    audit_log = AuditlogHistoryField()
    slug = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    registered_date = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        blank=True
    )

    def __str__(self):
        return self.name


@auditlog.register()
class Sample(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    audit_log = AuditlogHistoryField()
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50, default="default")
    sample_type = models.ForeignKey(SampleType)
    request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    inventory = models.ForeignKey('Inventory', on_delete=models.CASCADE)
    registered_date = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        blank=True
    )

    def __str__(self):
        return self.name + ' | ' + str(self.sample_type)


@auditlog.register()
class Inventory(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    audit_log = AuditlogHistoryField()
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    registered_date = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        blank=True
    )

    def __str__(self):
        return self.name


@auditlog.register()
class InventoryItem(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    audit_log = AuditlogHistoryField()
    sample = models.ForeignKey(Sample)
    # name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    # location = models.CharField(max_length=200)
    # inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    state = models.CharField(max_length=100, null=True)
    # def __str__(self):
    #     return self.name
    registered_date = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        blank=True
    )


@auditlog.register()
class InventoryOrder(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    audit_log = AuditlogHistoryField()
    essay = models.ForeignKey(EssayFill)
    unsettled = models.BooleanField()
    registered_date = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        blank=True
    )


@auditlog.register()
class InventoryOrderDefault(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    audit_log = AuditlogHistoryField()
    detail = models.CharField(max_length=100)
    registered_date = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        blank=True
    )
