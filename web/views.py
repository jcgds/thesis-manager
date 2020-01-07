import operator
from functools import reduce

from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic.edit import CreateView

from . import forms
from .models import PersonData


def index(request):
    return HttpResponse("Hello, world. You're at the web index.")


def person_detail(request, person_id_card_number):
    person = get_object_or_404(PersonData, id_card_number=person_id_card_number)
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


def edit_person(request, person_id_card_number):
    return HttpResponse('Edit person %s' % person_id_card_number)


class PersonDataCreate(SuccessMessageMixin, CreateView):
    model = PersonData
    form_class = forms.PersonDataForm
    success_message = "%(id_card_number)s was created successfully"

    def form_valid(self, form):
        print('Valid form.')
        return super(PersonDataCreate, self).form_valid(form)

    def form_invalid(self, form):
        print('Invalid form.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('create_person')

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            id_card_number=self.object.id_card_number,
        )
