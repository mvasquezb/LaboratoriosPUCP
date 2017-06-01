from django import forms

from internal import models


class RoleForm(forms.ModelForm):
    class Meta:
        model = models.Role
        fields = ['description', 'access']


ParameterFillFormset = forms.modelformset_factory(
    models.ParameterFill,
    fields=('value',),
    extra=0
)
