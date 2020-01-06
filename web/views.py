from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import PersonData


def index(request):
    return HttpResponse("Hello, world. You're at the web index.")


def person_detail(request, person_id_card_number):
    person = get_object_or_404(PersonData, id_card_number=person_id_card_number)
    context = {
        'person_data': person
    }
    return render(request, 'web/person_detail.html', context)
