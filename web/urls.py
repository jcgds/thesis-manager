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
    path('tg/estados', views.thesis_status_index, name='thesis_status_index'),
    path('tg/estados/agregar', views.ThesisStatusCreate.as_view(), name='create_thesis_status'),
    path('tg/estados/<int:pk>/editar', views.ThesisStatusUpdate.as_view(), name='edit_thesis_status'),
]
