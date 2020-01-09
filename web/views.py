import operator
from functools import reduce

from dal import autocomplete
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView

from . import forms
from .decorators import manager_required
from .models import PersonData, PersonType, ThesisStatus, Thesis, Proposal, Term, Defence, ProposalStatus, HistoricThesisStatus

login_view = auth_views.LoginView.as_view(authentication_form=forms.UserLoginForm)
logout_view = auth_views.LogoutView.as_view()


def index(request):
    return render(request, 'web/landing.html')


def person_detail(request, pk):
    person = get_object_or_404(PersonData, pk=pk)
    context = {
        'person_data': person
    }
    return render(request, 'web/persons/person_detail.html', context)


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
    return render(request, 'web/persons/person_list.html', context)


@method_decorator([login_required, manager_required], name='dispatch')
class PersonDataCreate(SuccessMessageMixin, CreateView):
    model = PersonData
    form_class = forms.PersonDataForm
    template_name = 'web/persons/persondata_form.html'
    success_message = "%(id_card_number)s creado correctamente."

    def get_success_url(self):
        return reverse('create_person')

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            id_card_number=self.object.id_card_number,
        )


@method_decorator([login_required, manager_required], name='dispatch')
class PersonDataUpdate(SuccessMessageMixin, UpdateView):
    model = PersonData
    form_class = forms.PersonDataForm
    template_name = 'web/persons/persondata_form.html'
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
    return render(request, 'web/person_types/persontype_list.html', context)


@method_decorator([login_required, manager_required], name='dispatch')
class PersonTypeCreate(SuccessMessageMixin, CreateView):
    model = PersonType
    form_class = forms.PersonTypeForm
    template_name = 'web/person_types/persontype_form.html'
    success_message = "Tipo \"%(name)s\" creado correctamente."

    def get_success_url(self):
        return reverse('person_type_index')

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.name,
        )


@method_decorator([login_required, manager_required], name='dispatch')
class PersonTypeUpdate(SuccessMessageMixin, UpdateView):
    model = PersonType
    form_class = forms.PersonTypeForm
    template_name = 'web/person_types/persontype_form.html'
    success_message = "Tipo \"%(name)s\" editado correctamente."

    def get_success_url(self):
        return reverse('edit_person_type', args=(self.object.pk,))

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.name,
        )


# TODO: Fix name variables to fit the context
def thesis_status_index(request):
    search_param = request.GET.get('search')
    if search_param:
        # Setup to search in multiple fields, currently in only has one but in the future
        # it could have more searchable fields.
        search_args = []
        for term in search_param.split():
            for query in ('name__icontains',):
                search_args.append(Q(**{query: term}))
        thesis_status_list = ThesisStatus.objects.filter(reduce(operator.or_, search_args))
    else:
        # If we don't receive a search parameter, don't apply any filters
        thesis_status_list = ThesisStatus.objects.all().order_by('name')

    paginator = Paginator(thesis_status_list, request.GET.get('page_length', 15))
    page = request.GET.get('page')
    types_by_page = paginator.get_page(page)
    context = {
        'types': types_by_page,
        'search_form': forms.SearchForm(previous_search=search_param),
        'search_param': search_param,
    }
    return render(request, 'web/thesis_statuses/thesisstatus_list.html', context)


@method_decorator([login_required, manager_required], name='dispatch')
class ThesisStatusCreate(SuccessMessageMixin, CreateView):
    model = ThesisStatus
    form_class = forms.ThesisStatusForm
    template_name = 'web/thesis_statuses/thesisstatus_form.html'
    success_message = "Estado \"%(name)s\" creado correctamente."

    def get_success_url(self):
        return reverse('thesis_status_index')

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.name,
        )


@method_decorator([login_required, manager_required], name='dispatch')
class ThesisStatusUpdate(SuccessMessageMixin, UpdateView):
    model = ThesisStatus
    form_class = forms.ThesisStatusForm
    template_name = 'web/thesis_statuses/thesisstatus_form.html'
    success_message = "Estado \"%(name)s\" editado correctamente."

    def get_success_url(self):
        return reverse('edit_thesis_status', args=(self.object.pk,))

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.name,
        )


def thesis_index(request):
    search_param = request.GET.get('search')
    if search_param:
        # Append a query for each term received in the search parameters so that if we receive multiple
        # parameters, we crosscheck every single one with the colums id_card_number, name and last_name
        search_args = []
        for term in search_param.split():
            for query in ('code__icontains', 'NRC__icontains', 'title__icontains', 'status__name__icontains',
                          'thematic_category__icontains', 'proposal__title__icontains',
                          'proposal__student1__name__icontains', 'proposal__student1__last_name__icontains',
                          'proposal__student1__id_card_number__icontains', 'proposal__student2__name__icontains',
                          'proposal__student2__last_name__icontains', 'proposal__student2__id_card_number__icontains',
                          'proposal__academic_tutor__name__icontains', 'proposal__academic_tutor__last_name__icontains',
                          'proposal__academic_tutor__id_card_number__icontains',
                          'proposal__industry_tutor__name__icontains', 'proposal__industry_tutor__last_name__icontains',
                          'proposal__industry_tutor__id_card_number__icontains', 'delivery_term__name__icontains',):
                search_args.append(Q(**{query: term}))
            thesis_list = Thesis.objects.filter(reduce(operator.or_, search_args)).order_by(
                'proposal__student1__id_card_number').exclude(
                code__in=HistoricThesisStatus.objects.filter(status__name='Aprobado'))
    else:
        # If we don't receive a search parameter, don't apply any filters
        thesis_list = Thesis.objects.all().order_by('proposal__student1__id_card_number').exclude(
            code__in=HistoricThesisStatus.objects.filter(status__name='Aprobado').values('thesis__code'))

    for thesis in thesis_list:
        thesis = add_full_names(thesis)

    paginator = Paginator(thesis_list, request.GET.get('page_length', 15))
    page = request.GET.get('page')
    thesis_by_page = paginator.get_page(page)
    context = {
        'thesis_list': thesis_by_page,
        'search_form': forms.SearchForm(previous_search=search_param),
        'search_param': search_param
    }

    return render(request, 'web/thesis/thesis_list.html', context)


@method_decorator([login_required, manager_required], name='dispatch')
class PersonTypeAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = PersonType.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs


@method_decorator([login_required, manager_required], name='dispatch')
class ProposalAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Proposal.objects.all()

        if self.q:
            qs = qs.filter(title__icontains=self.q, code__icontains=self.q, student1__name__icontains=self.q,
                           student1__last_name__icontains=self.q, student1__id_card_number__icontains=self.q,
                           student2__name__icontains=self.q, student2__last_name__icontains=self.q,
                           student2__id_card_number__icontains=self.q)
        return qs


@method_decorator([login_required, manager_required], name='dispatch')
class TermAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Term.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs


@method_decorator([login_required, manager_required], name='dispatch')
class ThesisCreate(SuccessMessageMixin, CreateView):
    model = Thesis
    form_class = forms.ThesisForm
    template_name = 'web/thesis/thesis_form.html'
    success_message = "%(code)s creado correctamente."

    def get_success_url(self):
        return reverse('create_thesis')

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            code=self.object.code,
        )


@method_decorator([login_required, manager_required], name='dispatch')
class ThesisUpdate(SuccessMessageMixin, UpdateView):
    model = Thesis
    form_class = forms.ThesisForm
    template_name = 'web/thesis/thesis_form.html'
    success_message = "%(code)s editado correctamente."

    def get_success_url(self):
        return reverse('edit_thesis', args=(self.object.code,))

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            code=self.object.code,
        )


def thesis_detail(request, pk):
    thesis = get_object_or_404(Thesis, pk=pk)
    thesis = add_full_names(thesis)

    context = {
        'thesis_data': thesis
    }
    return render(request, 'web/thesis/thesis_detail.html', context)


def add_full_names(thesis):
    thesis.status = HistoricThesisStatus.objects.filter(thesis__code=thesis.code).order_by('-date')[0].status
    thesis.proposal.academic_tutor.full_name = "{} {}".format(thesis.proposal.academic_tutor.name,
                                                              thesis.proposal.academic_tutor.last_name)
    if thesis.proposal.industry_tutor:
        thesis.proposal.industry_tutor.full_name = "{} {}".format(thesis.proposal.industry_tutor.name,
                                                                  thesis.proposal.industry_tutor.last_name)
    thesis.proposal.student1.full_name = "{} {}".format(thesis.proposal.student1.name,
                                                        thesis.proposal.student1.last_name)
    if thesis.proposal.student2:
        thesis.proposal.student2.full_name = "{} {}".format(thesis.proposal.student2.name,
                                                            thesis.proposal.student2.last_name)
    return thesis


def _get_defence_queryset(filter_completed, search):
    order_params = [
        'thesis__proposal__student1__id_card_number',
        'thesis__proposal__student2__id_card_number',
    ]
    if search:
        # Append a query for each term received in the search parameters so that if we receive multiple
        # parameters, we crosscheck every single one with the colums id_card_number, name and last_name
        search_args = []
        for term in search.split():
            for query in ('code__icontains', 'grade__icontains', 'thesis__title__icontains'):
                search_args.append(Q(**{query: term}))
        queryset = Defence.objects.filter(reduce(operator.or_, search_args))
    else:
        # If we don't receive a search parameter, don't apply any filters
        queryset = Defence.objects.all()

    if filter_completed:
        queryset = queryset.filter(grade__isnull=True)

    return queryset.order_by(*order_params)


def _generate_defence_index_context(defence_queryset, page_length, desired_page, search):
    paginator = Paginator(defence_queryset, page_length)
    defences_for_page = paginator.get_page(desired_page)
    return {
        'defences': defences_for_page,
        'search_form': forms.SearchForm(previous_search=search),
        'search_param': search
    }


def defence_index(request):
    """
    List of all the registered defences.
    """
    search_param = request.GET.get('search')
    defence_list = _get_defence_queryset(False, search_param)
    page = request.GET.get('page')
    context = _generate_defence_index_context(defence_list, request.GET.get('page_length', 15), page, search_param)
    return render(request, 'web/defences/defence_list.html', context)


def pending_defence_index(request):
    """
    List of defences that haven't been graded yet.
    """
    search_param = request.GET.get('search')
    defence_list = _get_defence_queryset(True, search_param)
    page = request.GET.get('page')
    context = _generate_defence_index_context(defence_list, request.GET.get('page_length', 15), page, search_param)
    return render(request, 'web/defences/defence_list.html', context)


def proposal_index(request):
    search_param = request.GET.get('search')
    if search_param:
        # Append a query for each term received in the search parameters so that if we receive multiple
        # parameters, we crosscheck every single one with the colums id_card_number, name and last_name
        search_args = []
        for term in search_param.split():
            for query in ('code__icontains', 'title__icontains',):
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


@method_decorator([login_required, manager_required], name='dispatch')
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


@method_decorator([login_required, manager_required], name='dispatch')
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


@method_decorator([login_required, manager_required], name='dispatch')
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


@method_decorator([login_required, manager_required], name='dispatch')
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


@method_decorator([login_required, manager_required], name='dispatch')
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


@method_decorator([login_required, manager_required], name='dispatch')
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



def proposal_not_approved_list(request):
    proposal_list = Proposal.objects.select_related().exclude(proposal_status__name="Aprobado").order_by('student1__id_card_number')
    paginator = Paginator(proposal_list, request.GET.get('page_length', 15))
    page = request.GET.get('page')
    proposal_by_page = paginator.get_page(page)
    context = {
        'proposal_list': proposal_by_page
    }
    return render(request, 'web/proposal_not_approved_list.html', context)
