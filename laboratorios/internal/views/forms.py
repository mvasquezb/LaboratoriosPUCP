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


class ClientForm(ModelForm):
    class Meta:
        model = Client
        exclude =('username',)



class ParameterForm(ModelForm):
    class Meta:
        model = ParameterTemplate
        exclude = ()

ParameterFormSet = inlineformset_factory(TestTemplate, ParameterTemplate, form=ParameterForm, extra=1)

class EssayForm(ModelForm):
    class Meta:
        model = EssayTemplate
        fields = ['description']

class SampleForm(ModelForm):
    class Meta:
        model = SampleTemplate
        fields = ['description']

SampleFormSet = inlineformset_factory(ServiceRequest, SampleFill, form=SampleForm, extra=1)


class AccessForm(ModelForm):
    class Meta:
        model = Access
        fields = ["description"]
        widgets = {
            "description": TextInput()
        }


class ServiceRequestForm(ModelForm):
    class Meta:
        model = ServiceRequest
        exclude = ()
