from django.urls import path
from . import views

urlpatterns = [
    # ex: /parkinglist/
    path('', views.index, name='index'),
    # ex: /parkinglist/search
    path('parkinglist/search/', views.get_search, name='search'),
    # ex: /parkinglist/adv_search
    path('parkinglist/adv_search', views.adv_search, name='adv_search'),
]