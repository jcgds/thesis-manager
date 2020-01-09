from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('personas', views.person_index, name='person_index'),
    path('personas/tipos', views.person_type_index, name='person_type_index'),
    path('personas/tipos/agregar', views.PersonTypeCreate.as_view(), name='create_person_type'),
    path('personas/tipos/<int:pk>/editar', views.PersonTypeUpdate.as_view(), name='edit_person_type'),
    path('personas/agregar', views.PersonDataCreate.as_view(), name='create_person'),
    path('personas/<str:pk>', views.person_detail, name='person_detail'),
    path('personas/<str:pk>/editar', views.PersonDataUpdate.as_view(), name='edit_person'),
    path('personas/<str:person_id_card_number>', views.person_detail, name='person_detail'),
    path('propuestas', views.proposal_index, name='proposal_index'),
    path('propuestas/agregar', views.ProposalCreate.as_view(), name='create_proposal'),
    path('propuestas/<str:pk>/editar', views.ProposalEdit.as_view(), name='edit_proposal'),
    path('term/agregar', views.TermCreate.as_view(), name='term_create')
]
