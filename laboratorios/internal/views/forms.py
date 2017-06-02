from django.forms import ModelForm
from internal.models import *
from django.forms import ModelForm,Textarea,CheckboxSelectMultiple,TextInput
from django.forms import ModelMultipleChoiceField
from django.forms import inlineformset_factory
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
        fields = ['id', "name"]

class ParameterForm(ModelForm):
    class Meta:
        model = ParameterTemplate
        exclude = ()

ParameterFormSet = inlineformset_factory(TestTemplate, ParameterTemplate, form=ParameterForm, extra=1)

class AccessForm(ModelForm):
    class Meta:
        model = Access
        fields = ["description"]
        widgets = {
            "description": TextInput()
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


class EssayTemplateForm(ModelForm):
    class Meta:
        model = EssayTemplate
        #fields = ['code', 'test_number', 'description']
        fields = ['code', 'description']

    tests = forms.ModelMultipleChoiceField(queryset=TestTemplate.objects.all())

    # Overriding __init__ here allows us to provide initial
    def __init__(self, *args, **kwargs):
        # Only in case we build the form from an instance
        # (otherwise, 'toppings' list should be empty)
        if kwargs.get('instance'):
            # We get the 'initial' keyword argument or initialize it
            # as a dict if it didn't exist.
            initial = kwargs.setdefault('initial', {})
            # The widget for a ModelMultipleChoiceField expects
            # a list of primary key for the selected data.
            initial['tests'] = [t.pk for t in kwargs['instance'].tests.all()]


        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['tests'].required = False

    # Overriding save allows us to process the value of 'toppings' field
    def save(self, commit=True):
        # Get the unsave Pizza instance
        instance = forms.ModelForm.save(self, False)

        # Prepare a 'save_m2m' method for the form,
        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            # This is where we actually link the pizza with toppings
            instance.tests.clear()
            for test in self.cleaned_data['tests']:
                instance.tests.add(test)

        self.save_m2m = save_m2m

        # Do we need to save all changes now?
        if commit:
            instance.save()
            self.save_m2m()

        return instance

        # def __init__(self, *args, **kwargs):
        #     super(EssayTemplateForm, self).__init__(*args, **kwargs)
        #     if self.instance.pk:
        #         # if this is not a new object, we load related books
        #         self.initial['tests'] = self.instance.tests.values_list('pk', flat=True)
        #
        # def save(self, *args, **kwargs):
        #     instance = super(EssayTemplateForm, self).save(*args, **kwargs)
        #     if instance.pk:
        #         for test in instance.tests.all():
        #             print(self.cleaned_data['tests'])
        #             if test not in self.cleaned_data['tests']:
        #                 # we remove books which have been unselected
        #                 instance.tests.remove(test)
        #         for test in self.cleaned_data['tests']:
        #             if test not in instance.tests.all():
        #                 # we add newly selected books
        #                 instance.books.add(test)
        #     return instance