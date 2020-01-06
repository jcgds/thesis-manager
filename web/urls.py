from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('people/<str:person_id_card_number>', views.person_detail, name='person_detail')
]
