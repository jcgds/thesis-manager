import operator
from functools import reduce

from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView

from . import forms
from .models import PersonData, PersonType, Proposal, Term, ProposalStatus


def index(request):
    return HttpResponse("Hello, world. You're at the web index.")


def person_detail(request, pk):
    person = get_object_or_404(PersonData, pk=pk)
    context = {
        'person_data': person
    }
    return render(request, 'web/person_detail.html', context)


def person_index(request):
    search_param = request.GET.get('search')
    if search_param:
        # Append a query for each term received in the search parameters so that if we receive multiple
        # parameters, we crosscheck every single one with the colums id_card_number, name and last_name
        search_args = []
        for term in search_param.split():
            for query in ('id_card_number__icontains', 'name__icontains', 'last_name__icontains'):
                search_args.append(Q(**{query: term}))
        person_list = PersonData.objects.filter(reduce(operator.or_, search_args))
    else:
        # If we don't receive a search parameter, don't apply any filters
        person_list = PersonData.objects.all().order_by('id_card_number', 'name')

    paginator = Paginator(person_list, request.GET.get('page_length', 15))
    page = request.GET.get('page')
    persons_by_page = paginator.get_page(page)
    context = {
        'person_list': persons_by_page,
        'search_form': forms.SearchForm(previous_search=search_param),
        'search_param': search_param
    }
    return render(request, 'web/person_list.html', context)


class PersonDataCreate(SuccessMessageMixin, CreateView):
    model = PersonData
    form_class = forms.PersonDataForm
    success_message = "%(id_card_number)s creado correctamente."

    def get_success_url(self):
        return reverse('create_person')

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            id_card_number=self.object.id_card_number,
        )


class PersonDataUpdate(SuccessMessageMixin, UpdateView):
    model = PersonData
    form_class = forms.PersonDataForm
    success_message = "%(id_card_number)s editado correctamente."

    def get_success_url(self):
        return reverse('edit_person', args=(self.object.id_card_number,))

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            id_card_number=self.object.id_card_number,
        )


def person_type_index(request):
    search_param = request.GET.get('search')
    if search_param:
        # Setup to search in multiple fields, currently in only has one but in the future
        # it could have more searchable fields.
        search_args = []
        for term in search_param.split():
            for query in ('name__icontains',):
                search_args.append(Q(**{query: term}))
        person_type_list = PersonType.objects.filter(reduce(operator.or_, search_args))
    else:
        # If we don't receive a search parameter, don't apply any filters
        person_type_list = PersonType.objects.all().order_by('name')

    paginator = Paginator(person_type_list, request.GET.get('page_length', 15))
    page = request.GET.get('page')
    types_by_page = paginator.get_page(page)
    context = {
        'types': types_by_page,
        'search_form': forms.SearchForm(previous_search=search_param),
        'search_param': search_param,
    }
    return render(request, 'web/persontype_list.html', context)


class PersonTypeCreate(SuccessMessageMixin, CreateView):
    model = PersonType
    form_class = forms.PersonTypeForm
    success_message = "Tipo \"%(name)s\" creado correctamente."

    def get_success_url(self):
        return reverse('person_type_index')

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.name,
        )


class PersonTypeUpdate(SuccessMessageMixin, UpdateView):
    model = PersonType
    form_class = forms.PersonTypeForm
    success_message = "Tipo \"%(name)s\" editado correctamente."

    def get_success_url(self):
        return reverse('edit_person_type', args=(self.object.pk,))

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.name,
        )


def proposal_index(request):

    search_param = request.GET.get('search')
    if search_param:
        # Append a query for each term received in the search parameters so that if we receive multiple
        # parameters, we crosscheck every single one with the colums id_card_number, name and last_name
        search_args = []
        for term in search_param.split():
            for query in ('code__icontains','title__icontains',):
                search_args.append(Q(**{query: term}))
        proposal_list = Proposal.objects.filter(reduce(operator.or_, search_args))
    else:
        # If we don't receive a search parameter, don't apply any filters
        proposal_list = Proposal.objects.all().select_related().order_by('code')

    paginator = Paginator(proposal_list, request.GET.get('page_length', 15))
    page = request.GET.get('page')
    proposal_by_page = paginator.get_page(page)
    context = {
        'proposal_list': proposal_by_page,
        'search_form': forms.SearchForm(previous_search=search_param),
        'search_param': search_param
    }
    return render(request, 'web/proposal_list.html', context)


class ProposalCreate(SuccessMessageMixin, CreateView):
    model = Proposal
    form_class = forms.ProposalForm
    success_message = "%(code)s Creado correctamente."

    def get_success_url(self):
        return reverse('proposal_index')

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            code=self.object.code,
        )


class ProposalEdit(SuccessMessageMixin, UpdateView):
    model = Proposal
    form_class = forms.ProposalForm
    success_message = "%(code)s editado correctamente."

    def get_success_url(self):
        return reverse('edit_proposal', args=(self.object.code,))

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            code=self.object.code,
        )


def term_index(request):
    term_list = Term.objects.all()
    paginator = Paginator(term_list, request.GET.get('page_length', 15))
    page = request.GET.get('page')
    terms_by_page = paginator.get_page(page)
    context = {
        'term_list': terms_by_page
    }
    return render(request, 'web/term_list.html', context)


class TermCreate(SuccessMessageMixin, CreateView):
    model = Term
    form_class = forms.TermForm
    success_message = "periodo %(period)s creado correctamente."

    def get_success_url(self):
        return reverse('term_index')

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            period=self.object.period,
        )


class TermUpdate(SuccessMessageMixin, UpdateView):
    model = Term
    form_class = forms.TermForm
    success_message = "Periodo %(period)s editado correctamente."

    def get_success_url(self):
        return reverse('term_index')

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            code=self.object.period,
        )


def proposal_status_index(request):
    proposal_status_list = ProposalStatus.objects.all()
    paginator = Paginator(proposal_status_list, request.GET.get('page_length', 15))
    page = request.GET.get('page')
    proposal_status_by_page = paginator.get_page(page)
    context = {
        'proposal_status_list': proposal_status_by_page
    }
    return render(request, 'web/proposal_status_list.html', context)


class ProposalStatusCreate(SuccessMessageMixin, CreateView):
    model = ProposalStatus
    form_class = forms.ProposalStatusForm
    success_message = "Estatus %(name)s creado correctamente."

    def get_success_url(self):
        return reverse('proposal_status_index')

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            period=self.object.name,
        )


class ProposalStatusUpdate(SuccessMessageMixin, UpdateView):
    model = ProposalStatus
    form_class = forms.ProposalStatusForm
    success_message = "Estatus %(name)s editado correctamente."

    def get_success_url(self):
        return reverse('proposal_status_index')

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.name,
        )