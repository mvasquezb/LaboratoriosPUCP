from django.forms import ModelForm,Textarea,CheckboxSelectMultiple
from internal.models import Role
from internal.models import Access
from django.forms import ModelMultipleChoiceField


class RoleForm(ModelForm):
    class Meta:
        model = Role
        fields = ['description','access']
        widgets = {
            'description': Textarea(),
            'access': CheckboxSelectMultiple()
        }
