from django.urls import path
from .views import *

urlpatterns = [
    path('', cards_list, name='cars_list_url'),
    path('card/<str:card_number>/', card_detail, name='card_detail_url')
]