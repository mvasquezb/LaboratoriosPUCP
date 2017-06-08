from django.forms import ModelForm
from internal.models import *
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import ModelForm,Textarea,CheckboxSelectMultiple,TextInput
from django.forms import ModelMultipleChoiceField
from django.forms import inlineformset_factory
from django import forms
from django.forms.models import BaseInlineFormSet


class EmployeeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['roles'].required = False
        self.fields['laboratories'].required = False
        self.fields['username'].required = True
        self.fields['password'].required = True
    class Meta:
        model = Employee
        fields = ['username', 'email', 'roles', 'password', 'first_name', 'last_name']

    laboratories = forms.ModelMultipleChoiceField(queryset=Laboratory.objects.all())


class EssayFillForm(ModelForm):
    class Meta:
        model = EssayFill
        fields = ['essay']

EssayFillFormset = inlineformset_factory(Sample, EssayFill, form=EssayFillForm, extra=1)


class RequestForm(ModelForm):
    class Meta:
        model = ServiceRequest
        fields = '__all__'



class SampleForm(ModelForm):
    iquery = Essay.objects.values_list('name',flat=True).distinct()
    iquery_choices = [('', 'None')] + [(name,name) for name in iquery]
    essay_field = forms.ChoiceField(iquery_choices,required=False, widget=forms.Select())
    #essay_field= forms.ModelChoiceField(widget=forms.Select, queryset=Essay.objects.all().values())
    class Meta:
        model = Sample
        fields = ['name','sample_type','inventory','request']+['essay_field']


    def save(self, commit=True):
        sample = super(SampleForm,self).save(commit=commit)
        essay_selected = Essay.objects.filter(name=self.cleaned_data['essay_field'])[0]
        essay_fill_created = EssayFill(sample=sample)
        essay_fill_created.create(essay_selected)
        essay_fill_created.save()
        return super(SampleForm,self).save(commit=commit)
    
    


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['doc_number','username','phone_number']


class ServiceRequestForm(ModelForm):
    class Meta:
        model = ServiceRequest
        exclude = ()

class RoleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RoleForm,self).__init__( *args, **kwargs)
        self.fields['permissions'].required=True
        self.fields['name'].required=True
        self.fields['description'].required=False
    class Meta:
        model=Role
        fields = ['name','description']
    permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.all())

class EssayMethodFillChosenForm(ModelForm):
    class Meta:
        model = EssayMethodFill
        fields = ['chosen']

class SampleEditForm(ModelForm):
    class Meta:
        model = Sample
        fields = ['name','sample_type','inventory']

class EssayFillSelectionForm(ModelForm):
    class Meta:
        model = EssayFill
        fields = ['essay']