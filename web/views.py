from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import PersonData
from .models import Proposal


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
    query = Q(id_card_number__contains=id_or_name_filter) \
            | Q(name__contains=id_or_name_filter) \
            | Q(last_name__contains=id_or_name_filter)
    person_list = PersonData.objects.filter(query) if id_or_name_filter else PersonData.objects.all()
    paginator = Paginator(person_list, request.GET.get('page_length', 15))
    page = request.GET.get('page')
    persons_by_page = paginator.get_page(page)
    context = {
        'person_list': persons_by_page
    }
    return render(request, 'web/person_list.html', context)


def proposal_index(request):
    proposal_list = Proposal.objects.all().select_related()
    paginator = Paginator(proposal_list, request.GET.get('page_length', 15))
    page = request.GET.get('page')
    proposal_by_page = paginator.get_page(page)
    context = {
        'proposal_list': proposal_by_page
    }
    return render(request, 'web/proposal_list.html', context)
