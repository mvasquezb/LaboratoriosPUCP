from django.forms import ModelForm
from internal.models  import *
from django.forms import ModelForm,Textarea,CheckboxSelectMultiple
from django.forms import ModelMultipleChoiceField


class RoleForm(ModelForm):
    class Meta:
        model = Role
        fields = ['description', 'access']
        widgets = {
            'description': Textarea(),
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
