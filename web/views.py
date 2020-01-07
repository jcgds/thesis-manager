from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .forms import SearchForm
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
    id_or_name_filter = request.GET.get('search')
    query = Q(id_card_number__icontains=id_or_name_filter) \
            | Q(name__icontains=id_or_name_filter) \
            | Q(last_name__icontains=id_or_name_filter)
    person_list = PersonData.objects.filter(query) if id_or_name_filter else PersonData.objects.all()
    paginator = Paginator(person_list, request.GET.get('page_length', 15))
    page = request.GET.get('page')
    persons_by_page = paginator.get_page(page)
    search_param = request.GET.get('search')
    context = {
        'person_list': persons_by_page,
        'search_form': SearchForm(previous_search=search_param),
        'search_param': search_param
    }
    return render(request, 'web/person_list.html', context)
