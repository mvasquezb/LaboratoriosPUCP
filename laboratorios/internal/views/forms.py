from django.forms import ModelForm
from internal.models import *


class RoleForm(ModelForm):
    class Meta:
        model = Role
        fields = ['description', 'access']

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
