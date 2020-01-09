from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('personas', views.person_index, name='person_index'),
    path('personas/agregar', views.PersonDataCreate.as_view(), name='create_person'),
    path('personas/tipos', views.person_type_index, name='person_type_index'),
    path('tg/agregar', views.ThesisCreate.as_view(), name='create_thesis'),
    path('tg/estados', views.thesis_status_index, name='thesis_status_index'),
    path('personas/tipos/agregar', views.PersonTypeCreate.as_view(), name='create_person_type'),
    path('tg/estados/agregar', views.ThesisStatusCreate.as_view(), name='create_thesis_status'),
    path('personas/tipos/<int:pk>/editar', views.PersonTypeUpdate.as_view(), name='edit_person_type'),
    path('personas/<str:pk>', views.person_detail, name='person_detail'),
    path('personas/<str:pk>/editar', views.PersonDataUpdate.as_view(), name='edit_person'),
    path('defensas/', views.defence_index, name='defence_index'),
    path('tg', views.thesis_index, name='thesis_index'),
    path('tg/<str:pk>', views.thesis_detail, name='thesis_detail'),
    path('tg/<str:pk>/editar', views.ThesisUpdate.as_view(), name='edit_thesis'),
    path('tg/estados/<int:pk>/editar', views.ThesisStatusUpdate.as_view(), name='edit_thesis_status'),
    path('person-type-autocomplete', views.PersonTypeAutoComplete.as_view(), name='person-type-autocomplete'),
    path('proposal-autocomplete', views.ProposalAutocomplete.as_view(), name='proposal-autocomplete'),
    path('term-autocomplete', views.TermAutocomplete.as_view(), name='term-autocomplete'),
]
