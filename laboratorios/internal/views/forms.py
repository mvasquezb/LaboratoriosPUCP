from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms import (
    ModelForm,
)
from django.forms import inlineformset_factory
# from django.forms.models import BaseInlineFormSet
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import forms as auth_forms


from internal.models import *
import copy


class EmployeeForm(ModelForm):
    laboratories = forms.ModelMultipleChoiceField(
        queryset=Laboratory.all_objects.filter(deleted__isnull=True)
    )

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['roles'].required = False
        self.fields['laboratories'].required = False

    class Meta:
        model = Employee
        fields = ['roles']

    def _save_m2m(self, *args, **kwargs):
        super(EmployeeForm, self)._save_m2m(*args, **kwargs)
        self.instance.laboratories.set(self.cleaned_data['laboratories'])


class UserCreationForm(auth_forms.UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        if self.data and self.data.get('password1'):
            self.data = copy.copy(self.data)
            self.data['password2'] = self.data['password1']

    class Meta(auth_forms.UserCreationForm.Meta):
        fields = ('username', 'first_name', 'last_name', 'email')


class UserEditForm(auth_forms.UserChangeForm):
    # Override parent class 'password' field
    password = None

    class Meta(auth_forms.UserChangeForm.Meta):
        fields = ('username', 'first_name', 'last_name', 'email')


class EssayFillForm(ModelForm):
    class Meta:
        model = EssayFill
        fields = ['essay']


EssayFillFormset = inlineformset_factory(
    Sample, EssayFill, form=EssayFillForm, extra=1)


class RequestForm(ModelForm):
    class Meta:
        model = ServiceRequest
        fields = '__all__'


class SampleForm(ModelForm):
    # iquery = Essay.objects.values_list('name',flat=True).distinct()
    # iquery_choices = [('', 'None')] + [(name,name) for name in iquery]
    # essay_field = forms.ChoiceField(iquery_choices,required=False, widget=forms.Select())
    essay_field = forms.ModelChoiceField(
        queryset=Essay.all_objects.filter(deleted__isnull=True)
    )

    class Meta:
        model = Sample
        fields = ['name', 'sample_type', 'inventory', 'request', 'essay_field']

    def save(self, commit=True):
        sample = super(SampleForm, self).save(commit=commit)
        essay_selected = Essay.all_objects.filter(
            deleted__isnull=True,
            name=self.cleaned_data['essay_field']
        )[0]
        essay_fill_created = EssayFill(sample=sample)
        essay_fill_created.create(essay_selected)
        essay_fill_created.save()
        return super(SampleForm, self).save(commit=commit)


class ClientForm(ModelForm):
    class Meta:
        model = Client
        # fields = ['doc_number', 'username', 'phone_number']
        fields = ('doc_number', 'phone_number')


class ServiceRequestForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ServiceRequestForm, self).__init__(*args, **kwargs)
        self.fields['client'].widget.attrs['class'] = 'form-control'
        self.fields['supervisor'].widget.attrs['class'] = 'form-control'
        self.fields['state'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = ServiceRequest
        exclude = ()


class RoleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)
        self.fields['permissions'].required = True
        self.fields['name'].required = True
        self.fields['description'].required = False

    class Meta:
        model = Role
        fields = ['name', 'description']
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.all_objects.filter(deleted__isnull=True))


class EssayMethodFillChosenForm(ModelForm):
    class Meta:
        model = EssayMethodFill
        fields = ['chosen', ]


class SampleEditForm(ModelForm):
    class Meta:
        model = Sample
        fields = ['name', 'sample_type', 'inventory']


class EssayFillSelectionForm(ModelForm):
    class Meta:
        model = EssayFill
        fields = ['essay']

    def save(self, commit=True):
        # verify that methods belong to particular essay
        myself = super(EssayFillSelectionForm, self).save(commit=commit)
        essay = Essay.all_objects.get(
            deleted__isnull=True,
            pk=self.data['essay']
        )
        EssayFill.all_objects.filter(
            deleted__isnull=True,
            essay=myself.essay
        )
        methods_count = essay_fills
        essay_methods = EssayMethod.all_objects.filter(
            deleted__isnull=True,
            essays=essay
        )
        if methods_count == essay_methods.count():
            essay_fill_methods = EssayFill.all_objects.filter(
                deleted__isnull=True,
                essay=myself.essay
            )
            exit_loop = 0
            for i in range(0, methods_count):
                if (essay_fill_methods[i].essay_method == essay_methods[i]):
                    pass
                else:
                    exit_loop += 1
            if exit_loop == 0:
                return super(EssayFillSelectionForm, self).save(commit=commit)
        # if it goes beyond this line, it means it has selected a new essay to
        # use as template
        myself.recreate(essay)
        return super(EssayFillSelectionForm, self).save(commit=commit)


class ServiceAssignEmployeeForm(forms.Form):
    employee = forms.ModelChoiceField(queryset=Employee.all_objects.filter(
        deleted__isnull=True
    ))

    def __init__(self, *args, **kwargs):
        employee = None
        if 'employee' in kwargs:
            employee = kwargs.pop('employee')
        super().__init__(*args, **kwargs)
        if employee is not None:
            self.fields['employee'].queryset = employee


class LaboratoryForm(ModelForm):
    class Meta:
        model = Laboratory
        exclude = []


class SampleTypeForm(ModelForm):
    class Meta:
        model = SampleType
        exclude = ['slug']


class InventoryOrderForm(ModelForm):
    class Meta:
        model = InventoryOrder
        fields = ['essay', 'unsettled']


class InventoryOrderEditForm(ModelForm):
    class Meta:
        model = InventoryOrder
        fields = ('essay',)


class EssayForm(ModelForm):
    class Meta:
        model = Essay
        exclude = ['essay_methods']


class LongCharField(models.CharField):
    "A basically unlimited-length CharField."
    description = _("Unlimited-length string")
    label = 'None'

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = int(1e9)  # Satisfy management validation.
        self.label = kwargs['label']
        super(models.CharField, self).__init__(*args, **kwargs)
        # Don't add max-length validator like CharField does.

    def get_internal_type(self):
        # This has no function, since this value is used as a lookup in
        # db_type().  Put something that isn't known by django so it
        # raises an error if it is ever used.
        return 'LongCharField'

    def db_type(self, connection):
        # *** This is probably only compatible with Postgres.
        # 'varchar' with no max length is equivalent to 'text' in Postgres,
        # but put 'varchar' so we can tell LongCharFields from TextFields
        # when we're looking at the db.
        return 'varchar'

    def formfield(self, **kwargs):
        # Don't pass max_length to form field like CharField does.
        return super(models.CharField, self).formfield(**kwargs)


class JSONField(forms.Form):
    js_data = forms.CharField(label='js_data')


class EssayMethodForm(ModelForm):
    class Meta:
        model = EssayMethod
        fields = ["name", "description", "price"]
