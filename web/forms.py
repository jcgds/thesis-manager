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


class PersonDataForm(forms.ModelForm):
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

    form_control_attr = {'class': 'form-control'}
    id_card_number = forms.CharField(
        label='Cédula',
        widget=forms.TextInput(attrs=form_control_attr)
    )
    name = forms.CharField(
        label='Nombres',
        widget=forms.TextInput(attrs=form_control_attr)
    )
    last_name = forms.CharField(
        label='Apellidos',
        widget=forms.TextInput(attrs=form_control_attr)
    )
    primary_phone_number = forms.CharField(
        label='Teléfono principal',
        widget=forms.TextInput(attrs=form_control_attr)
    )
    secondary_phone_number = forms.CharField(
        label='Teléfono secundario',
        required=False,
        widget=forms.TextInput(attrs=form_control_attr)
    )
    email = forms.EmailField(
        label='Correo personal',
        widget=forms.EmailInput(attrs=form_control_attr)
    )
    ucab_email = forms.EmailField(
        label='Correo UCAB',
        required=False,
        widget=forms.EmailInput(attrs=form_control_attr)
    )
    type = forms.ChoiceField(
        label='Tipo',
        choices=models.PersonData.TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control m-b'}))
    observations = forms.CharField(
        label='Observaciones',
        max_length=1_024,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
