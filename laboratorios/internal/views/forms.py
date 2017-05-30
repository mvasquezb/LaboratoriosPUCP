from django.forms import ModelForm
from internal.models  import *


class RoleForm(ModelForm):
    class Meta:
        model = Role
        fields = ['description', 'access']


class TestForm(ModelForm):
    class Meta:
        model = TestTemplate
        fields = ['id', 'description']
