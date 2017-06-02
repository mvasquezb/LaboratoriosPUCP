from django.forms import ModelForm
from internal.models import *
from django.forms import ModelForm,Textarea,CheckboxSelectMultiple,TextInput
from django.forms import ModelMultipleChoiceField
from django.forms import inlineformset_factory
from django import forms

class RoleForm(ModelForm):
    class Meta:
        model = Role
        fields = ["description", 'access']
        widgets = {
            "description": TextInput(),
            'access': CheckboxSelectMultiple()
        }

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'surname',
            'username',
            'address',
            'phone',
            'email',
            'laboratories',
            'password'
        ]

class TestForm(ModelForm):
    class Meta:
        model = TestTemplate
        fields = ['id', "name"]






class ParameterForm(ModelForm):
    class Meta:
        model = ParameterTemplate
        exclude = ()

ParameterFormSet = inlineformset_factory(TestTemplate, ParameterTemplate, form=ParameterForm, extra=1)

class AccessForm(ModelForm):
    class Meta:
        model = Access
        fields = ["description"]
        widgets = {
            "description": TextInput()
        }


