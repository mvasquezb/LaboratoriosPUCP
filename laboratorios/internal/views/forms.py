from django.forms import ModelForm
from internal.models  import *
from django.forms import ModelForm,Textarea,CheckboxSelectMultiple,TextInput
from django.forms import ModelMultipleChoiceField



class RoleForm(ModelForm):
    class Meta:
        model = Role
        fields = ['description', 'access']
        widgets = {
            'description': TextInput(),
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
        fields = ['id', 'description']

class AccessForm(ModelForm):
    class Meta:
        model = Access
        fields = ['description']
        widgets = {
            'description': TextInput()
        }

class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = [
            'name',
            'idDoc',
            'username',
            'phoneNumber'
        ]
