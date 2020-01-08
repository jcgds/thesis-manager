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
