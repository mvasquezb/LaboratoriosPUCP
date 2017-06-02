from django import forms

from internal import models


class RoleForm(forms.ModelForm):
    class Meta:
        model = models.Role
        fields = ['description', 'access']
        # widgets = {
        #     'description': TextInput(),
        #     'access': CheckboxSelectMultiple()
        # }


ParameterFillFormset = forms.modelformset_factory(
    models.ParameterFill,
    fields=('value',),
    extra=0
)


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = models.Employee
        fields = [
            'first_name',
            'last_name',
            'username',
            'address',
            'phone',
            'email',
            'laboratories',
            'password'
        ]


class TestForm(forms.ModelForm):
    class Meta:
        model = models.TestTemplate
        fields = ['id', 'description']


class AccessForm(forms.ModelForm):
    class Meta:
        model = models.Access
        fields = ['description']


class ClientForm(forms.ModelForm):
    class Meta:
        model = models.Client
        fields = [
            'name',
            'idDoc',
            'user',
            'phone'
        ]
