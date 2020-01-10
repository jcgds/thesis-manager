import operator
import statistics
from dal import autocomplete
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from functools import reduce

from . import forms
from .decorators import manager_required
from .models import PersonData, PersonType, ThesisStatus, Thesis, Proposal, Term, Defence, ProposalStatus, HistoricThesisStatus, Jury
from .render import render_to_pdf

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
        proposals_with_thesis = list(map(lambda thesis: thesis.proposal.code, Thesis.objects.all()))
        qs = Proposal.objects.exclude(code__in=proposals_with_thesis)

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


class PersonAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        persons = PersonData.objects.all()
        search_args = []
        for term in self.q.split():
            for query in ('id_card_number__icontains', 'name__icontains', 'last_name__icontains'):
                search_args.append(Q(**{query: term}))

        if search_args:
            persons = persons.filter(reduce(operator.or_, search_args))
        return persons


class TeacherAutoComplete(PersonAutoComplete):
    def get_queryset(self):
        qs = super().get_queryset()
        teacher_type = PersonType.objects.get(name='Profesor')
        return qs.filter(type=teacher_type)


class StudentAutoComplete(PersonAutoComplete):
    def get_queryset(self):
        qs = super().get_queryset()
        student_type = PersonType.objects.get(name='Estudiante')
        return qs.filter(type=student_type)


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


def proposal_detail(request, pk):
    proposal = get_object_or_404(Proposal, pk=pk)
    context = {
        'proposal_data': proposal
    }
    return render(request, 'web/proposal/proposal_detail.html', context)


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
    return render(request, 'web/proposal/proposal_list.html', context)


@method_decorator([login_required, manager_required], name='dispatch')
class ProposalCreate(SuccessMessageMixin, CreateView):
    model = Proposal
    form_class = forms.ProposalForm
    template_name = 'web/proposal/proposal_form.html'
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
    template_name = 'web/proposal/proposal_form.html'
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
    return render(request, 'web/term/term_list.html', context)


@method_decorator([login_required, manager_required], name='dispatch')
class TermCreate(SuccessMessageMixin, CreateView):
    model = Term
    form_class = forms.TermForm
    template_name = 'web/term/term_form.html'
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
    template_name = 'web/term/term_form.html'
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
    return render(request, 'web/proposal/proposal_status_list.html', context)


@method_decorator([login_required, manager_required], name='dispatch')
class ProposalStatusCreate(SuccessMessageMixin, CreateView):
    model = ProposalStatus
    form_class = forms.ProposalStatusForm
    template_name = 'web/proposal/proposalstatus_form.html'
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
    template_name = 'web/proposal/proposalstatus_form.html'
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
    return render(request, 'web/proposal/proposal_not_approved_list.html', context)


def stats_view(request):
    if request.method == 'POST':
        form = forms.StatsForm(request.POST)
        if form.is_valid():
            term_list = form.cleaned_data['terms']
            thesis_for_terms = Thesis.objects.filter(delivery_term__in=term_list)
            defences_for_thesis = Defence.objects.filter(thesis__in=thesis_for_terms).filter(grade__isnull=False)
            grades = list(map(lambda defence: defence.grade, defences_for_thesis))
            context = {
                'term_form': forms.StatsForm(),
                'term_list': term_list,
                'defence_list': defences_for_thesis,
                'grade_mean': statistics.mean(grades) if len(grades) > 0 else '-',
                'median_grade': statistics.median(grades) if len(grades) > 0 else '-',
                'mode': statistics.mode(grades) if len(grades) > 0 else '-',
                'standard_deviation': statistics.stdev(grades) if len(grades) > 1 else '-',
            }
            return render(request, 'web/stats/stats.html', context)
    else:
        context = {
            'term_form': forms.StatsForm(),
        }
        return render(request, 'web/stats/stats.html', context)


@method_decorator([login_required, manager_required], name='dispatch')
class ThesisAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        queryset = Thesis.objects.all()
        if self.q:
            queryset = queryset.filter(
                title__icontains=self.q,
                code__icontains=self.q,
                proposal__code=self.q,
                delivery_term__period__exact=self.q,
                NRC__icontains=self.q,
                thematic_category__icontains=self.q,
                submission_date__exact=self.q,
                company_name__icontains=self.q,
            )
        return queryset


@method_decorator([login_required, manager_required], name='dispatch')
class DefenceCreate(SuccessMessageMixin, CreateView):
    model = Defence
    form_class = forms.DefenceForm
    template_name = 'web/defences/defence_form.html'
    success_message = "Defensa \"%(code)s\" creada correctamente."

    def get_success_url(self):
        return reverse('create_defence')

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            code=self.object.code,
        )


@method_decorator([login_required, manager_required], name='dispatch')
class DefenceUpdate(SuccessMessageMixin, UpdateView):
    model = Defence
    form_class = forms.DefenceForm
    template_name = 'web/defences/defence_form.html'
    success_message = "Defensa \"%(code)s\" editada correctamente."

    def get_success_url(self):
        return reverse('update_defence', args=(self.object.code,))

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            code=self.object.code,
        )


@method_decorator([login_required, manager_required], name='dispatch')
class JuryCreate(SuccessMessageMixin, CreateView):
    model = Jury
    form_class = forms.JudgeForm
    template_name = 'web/defences/judge_form.html'
    success_message = "Juez \"%(pk)s\" creada correctamente."

    def get_success_url(self):
        return reverse('create_jury')

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            pk=self.object.pk,
        )


@method_decorator([login_required, manager_required], name='dispatch')
class JuryUpdate(SuccessMessageMixin, UpdateView):
    model = Jury
    form_class = forms.JudgeForm
    template_name = 'web/defences/judge_form.html'
    success_message = "Juez \"%(pk)s\" actualizado correctamente."

    def get_success_url(self):
        return reverse('update_jury', args=(self.object.pk,))

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            pk=self.object.pk,
        )


@method_decorator([login_required, manager_required], name='dispatch')
class JuryDelete(DeleteView):
    model = Jury
    success_url = reverse_lazy('defence_index')


class ProposalNotApprovedPdf(View):
    def get(self, request, *args, **kwargs):
        proposal_list = Proposal.objects.select_related().exclude(proposal_status__name="Aprobado").order_by('student1__id_card_number')
        context = {
            "proposal_list": proposal_list,
        }
        pdf = render_to_pdf('web/proposal/proposal_not_approved_pdf.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "ProposalsNotApproved.pdf"
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


class ProposalPdf(View):
    def get(self, request, *args, **kwargs):
        proposal_list = Proposal.objects.all().select_related()
        context = {
            "proposal_list": proposal_list,
        }
        pdf = render_to_pdf('web/proposal/proposal_pdf.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Proposals.pdf"
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


class PersonsListPdf(View):
    def get(self, request, *args, **kwargs):
        person_list = PersonData.objects.all().order_by('id_card_number', 'name')
        context = {
            "person_list": person_list,
        }
        pdf = render_to_pdf('web/persons/person_list_pdf.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Persons_list.pdf"
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")

