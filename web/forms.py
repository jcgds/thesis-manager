import re

from django import forms

from . import models


class SearchForm(forms.Form):

    def __init__(self, placeholder='Buscar', previous_search=None, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        field_attrs = {
            'class': 'form-control form-control-sm',
            'placeholder': placeholder
        }
        if previous_search:
            field_attrs['value'] = previous_search
        self.fields['search'].widget = forms.TextInput(attrs=field_attrs)

    search = forms.CharField(required=False, label='')


def _validate_phone_number(phone):
    pattern = re.compile("^[+]*[(]?[0-9]{1,4}[)]?[-\s./0-9]*$")
    if phone and not pattern.match(phone):
        raise forms.ValidationError('Número de teléfono inválido')


class PersonDataForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PersonDataForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['id_card_number'].widget.attrs['readonly'] = True

    class Meta:
        model = models.PersonData
        fields = [
            'id_card_number',
            'name',
            'last_name',
            'primary_phone_number',
            'secondary_phone_number',
            'email',
            'ucab_email',
            'type',
            'observations',
        ]

    id_card_number = forms.CharField(
        label='Cédula',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'V26691598'})
    )
    name = forms.CharField(
        label='Nombres',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Steph Meck'})
    )
    last_name = forms.CharField(
        label='Apellidos',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Collier Reese'})
    )
    primary_phone_number = forms.CharField(
        label='Teléfono principal',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+58 212 532 6912'})
    )
    secondary_phone_number = forms.CharField(
        label='Teléfono secundario',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+58 424 582 1902'})
    )
    email = forms.EmailField(
        label='Correo personal',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'steph.collier@gmail.com'})
    )
    ucab_email = forms.EmailField(
        label='Correo UCAB',
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'sc.collier16@ucab.edu.ve'})
    )
    type = forms.ModelChoiceField(
        label='Tipo',
        initial=0,
        queryset=models.PersonType.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control m-b'}))
    observations = forms.CharField(
        label='Observaciones',
        max_length=1_024,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    def clean_id_card_number(self):
        data = self.cleaned_data['id_card_number']
        pattern = re.compile("^[VE][0-9]+$")
        if not pattern.match(data):
            raise forms.ValidationError('La cédula debe comenzar por V o E seguida únicamente de dígitos')
        return data

    def clean_ucab_email(self):
        data = self.cleaned_data['ucab_email']
        if data and not data.endswith('ucab.edu.ve'):
            raise forms.ValidationError('El correo UCAB debe pertenecer al dominio ucab.edu.ve')
        return data

    def clean_primary_phone_number(self):
        data = self.cleaned_data['primary_phone_number']
        _validate_phone_number(data)
        return data

    def clean_secondary_phone_number(self):
        data = self.cleaned_data['secondary_phone_number']
        _validate_phone_number(data)
        return data
