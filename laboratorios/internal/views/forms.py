from django.forms import ModelForm
from internal.models import Role


class RoleForm(ModelForm):
    class Meta:
        model = Role
        fields = ['description', 'access']
