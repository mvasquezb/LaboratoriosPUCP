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

class TestForm(ModelForm):
    class Meta:
        model = TestTemplate
        fields = ['id', 'description']
