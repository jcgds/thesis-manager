from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('personas', views.person_index, name='person_index'),
    path('personas/agregar', views.PersonDataCreate.as_view(), name='create_person'),
    path('personas/<str:person_id_card_number>', views.person_detail, name='person_detail'),
    path('personas/<str:person_id_card_number>/editar', views.edit_person, name='edit_person'),
]
