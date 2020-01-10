import re
from datetime import datetime

from dal import autocomplete
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone

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
        widget=forms.Select(attrs={'class': 'form-control m-b'})
    )
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
        if instance and instance.pk:
            self.fields['proposal'].disabled = True
            self.fields['submission_date'].disabled = True

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
        initial=0,
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
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Inteligencia de negocios'})
    )
    submission_date = forms.DateField(
        label='Fecha de Inicio',
        widget=forms.SelectDateWidget(attrs={'twelve_hr': True}),
        initial=datetime.now()
    )
    company_name = forms.CharField(
        label='Compañia',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Estudio Chaloupka'})
    )

    def save(self, commit=True):
        thesis = super().save(commit)
        print(thesis)
        status = models.ThesisStatus.objects.get(name=self.cleaned_data['status'])
        print(status)
        models.HistoricThesisStatus(
            thesis=thesis,
            status=status
        ).save()
        return thesis


class ProposalForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProposalForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['code'].widget.attrs['readonly'] = True

    class Meta:
        model = models.Proposal
        fields = [
            'code',
            'submission_date',
            'title',
            'student1',
            'student2',
            'academic_tutor',
            'industry_tutor',
            'term',
            'proposal_status'
        ]

    code = forms.CharField(
        label='Codigo',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    submission_date = forms.DateField(
        label='Fecha de entrega',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    title = forms.CharField(
        label='Titulo',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    student1 = forms.ModelChoiceField(
        label='Primer Estudiante',
        queryset=models.PersonData.objects.filter(type__name='Estudiante'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    student2 = forms.ModelChoiceField(
        label='Segundo Estudiante',
        queryset=models.PersonData.objects.filter(type__name='Estudiante'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    academic_tutor = forms.ModelChoiceField(
        label='Tutor Academico',
        queryset=models.PersonData.objects.filter(type__name='Profesor'),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    industry_tutor = forms.ModelChoiceField(
        label='Tutor Industrial',
        queryset=models.PersonData.objects.filter(type__name='Externo'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    term = forms.ModelChoiceField(
        label='Term',
        queryset=models.Term.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    proposal_status = forms.ModelChoiceField(
        label='Status de la propuesta',
        queryset=models.ProposalStatus.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class TermForm(forms.ModelForm):
    class Meta:
        model = models.Term
        fields = [
            'period',
        ]

    period = forms.IntegerField(
        label='Periodo',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '999999'})
    )


class ProposalStatusForm(forms.ModelForm):
    class Meta:
        model = models.ProposalStatus
        fields = [
            'name',
            'description',
        ]

    name = forms.CharField(
        label='Nombre',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    description = forms.CharField(
        label='Descripcion',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


class StatsForm(forms.Form):
    terms = forms.ModelMultipleChoiceField(
        required=True,
        label='',
        queryset=models.Term.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control m-b'})
    )


class DefenceForm(forms.ModelForm):
    class Meta:
        model = models.Defence
        fields = [
            'thesis',
            'date_time',
            'grade',
            'is_publication_mention',
            'is_honorific_mention',
            'corrections_submission_date',
            'observations',
        ]

    thesis = forms.ModelChoiceField(
        label='Trabajo de grado',
        initial=0,
        queryset=models.Thesis.objects.all(),
        widget=autocomplete.ModelSelect2(url='thesis-autocomplete')
    )
    date_time = forms.DateTimeField(
        label='Fecha y hora de la presentación',
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            },
            format='%Y-%m-%dT%H:%M'
        )
    )
    grade = forms.IntegerField(
        label='Calificación',
        min_value=0,
        max_value=20,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    is_publication_mention = forms.BooleanField(
        label='Mención publicación',
        required=False,
        widget=forms.CheckboxInput(attrs={'type': 'checkbox'})
    )
    is_honorific_mention = forms.BooleanField(
        label='Mención honorífica',
        required=False,
        widget=forms.CheckboxInput(attrs={'type': 'checkbox'})
    )
    observations = forms.CharField(
        label='Observaciones',
        max_length=1_048,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    jury = forms.ModelMultipleChoiceField(
        label='Jurado',
        required=False,
        queryset=models.PersonData.objects.all(),  # This query is ignored
        widget=autocomplete.Select2Multiple(url='teacher-autocomplete', attrs={'class': 'form-control'})
    )

    def clean_date_time(self):
        form_datetime = self.cleaned_data['date_time']
        if form_datetime < timezone.now():
            raise forms.ValidationError("La fecha debe ser en el futuro.")
        return form_datetime

    def clean_jury(self):
        form_jury = self.cleaned_data['jury']
        if len(form_jury) > models.Defence.MAX_JUDGES:
            raise forms.ValidationError("Límite de jueces superado (Máximo %d)." % models.Defence.MAX_JUDGES)

        # If we are updating an instance
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            registered_judges = instance.get_complete_jury()
            if len(registered_judges) + len(form_jury) > models.Defence.MAX_JUDGES:
                raise forms.ValidationError("Límite de jueces superado (Máximo %d)." % models.Defence.MAX_JUDGES)

        return form_jury

    def save(self, commit=True):
        instance = super().save(commit=False)
        form_jury = self.cleaned_data['jury']
        for judge in form_jury:
            models.Jury(person=judge, defence=instance).save()
        if commit:
            instance.save()
        return instance


class JudgeForm(forms.ModelForm):
    class Meta:
        model = models.Jury
        fields = ['person', 'defence', 'is_backup_jury', 'confirmed_assistance']

    person = forms.ModelChoiceField(
        label='Profesor',
        initial=0,
        queryset=models.PersonData.objects.all(),  # Ignored
        widget=autocomplete.ModelSelect2(url='teacher-autocomplete')
    )
    defence = forms.ModelChoiceField(
        label='Defensa',
        initial=0,
        queryset=models.Defence.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    is_backup_jury = forms.BooleanField(
        label='Suplente',
        required=False,
        widget=forms.CheckboxInput(attrs={'type': 'checkbox'})
    )
    confirmed_assistance = forms.BooleanField(
        label='Va a asistir',
        required=False,
        widget=forms.CheckboxInput(attrs={'type': 'checkbox'})
    )
