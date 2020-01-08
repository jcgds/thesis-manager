from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('personas', views.person_index, name='person_index'),
    path('personas/agregar', views.PersonDataCreate.as_view(), name='create_person'),
    path('personas/<str:pk>', views.person_detail, name='person_detail'),
    path('personas/<str:pk>/editar', views.PersonDataUpdate.as_view(), name='edit_person'),
]
