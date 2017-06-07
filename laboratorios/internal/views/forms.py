from django.forms import ModelForm
from internal.models import *
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import NON_FIELD_ERRORS


class EmployeeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['roles'].required = False
        self.fields['laboratories'].required = False
        self.fields['username'].required = True
        self.fields['password'].required = True
    class Meta:
        model = Employee
        fields = ['username', 'email', 'roles', 'password', 'first_name', 'last_name']

    laboratories = forms.ModelMultipleChoiceField(queryset=Laboratory.objects.all())

class RoleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RoleForm,self).__init__( *args, **kwargs)
        self.fields['permissions'].required=True
        self.fields['name'].required=True
        self.fields['description'].required=False
    class Meta:
        model=Role
        fields = ['name','description']
    permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.all())
