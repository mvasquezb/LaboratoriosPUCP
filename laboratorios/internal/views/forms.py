from django.forms import ModelForm, TextInput, CheckboxSelectMultiple
from ..models import *


class RoleForm(ModelForm):
    class Meta:
        model = Role
        fields = ['description', 'access']
