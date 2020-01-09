import re
from datetime import datetime

from dal import autocomplete
from django import forms
from django.contrib.auth.forms import AuthenticationForm

from . import models


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Nombre de usuario',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu nombre de usuario'})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )


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


class PersonTypeForm(forms.ModelForm):
    class Meta:
        model = models.PersonType
        fields = ['name']

    name = forms.CharField(
        label='Nombre del rol',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Profesor'})
    )


class ThesisStatusForm(forms.ModelForm):
    class Meta:
        model = models.ThesisStatus
        fields = ['name']

    name = forms.CharField(
        label='Nombre del estado',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Por entregar'})
    )


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
        initial=1,
        queryset=models.PersonType.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control m-b'}))
    observations = forms.CharField(
        label='Observaciones',
        max_length=1_048,
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


class ThesisForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ThesisForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

    class Meta:
        model = models.Thesis
        fields = [
            'NRC',
            'title',
            'proposal',
            'status',
            'delivery_term',
            'description',
            'thematic_category',
            'submission_date',
            'company_name'
        ]

    NRC = forms.CharField(
        label='NRC',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '25960'})
    )
    title = forms.CharField(
        label='Título',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'This Is It'})
    )
    proposal = forms.ModelChoiceField(
        label='Propuesta',
        initial=1,
        queryset=models.Proposal.objects.all(),
        widget=autocomplete.ModelSelect2(url='proposal-autocomplete')
    )
    status = forms.ModelChoiceField(
        label='Estado',
        initial=0,
        queryset=models.ThesisStatus.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control m-b'})
    )
    delivery_term = forms.ModelChoiceField(
        label='Semestre de Entrega',
        initial=1,
        queryset=models.Term.objects.all(),
        widget=autocomplete.ModelSelect2(url='term-autocomplete')
    )
    description = forms.CharField(
        label='Descripción',
        max_length=1_024,
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': 'Software de registro de marcas', 'rows': 3})
    )

    thematic_category = forms.CharField(
        label='Categoria temática',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Inteligencia Artificial'})
    )
    submission_date = forms.DateField(
        label='Fecha de Inicio',
        widget=forms.SelectDateWidget(attrs={'twelve_hr': True}),
        initial=datetime.now()
    )
    company_name = forms.CharField(
        label='Compañia',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'DaycoHost'})
    )
