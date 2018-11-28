from django.urls import path
from . import views

urlpatterns = [
    # ex: /parkinglist/
    path('', views.index, name='index'),
    # ex: /A10
    path('<str:show>', views.index, name='index'),
    # ex: /parkinglist/search
    path('parkinglist/search', views.get_search, name='search'),
    path('parkinglist/search/', views.get_search, name='search'),
    # ex: /parkinglist/adv_search
    path('parkinglist/adv_search', views.adv_search, name='adv_search'),
    path('parkinglist/adv_search/', views.adv_search, name='adv_search'),
    # ex: /parkinglist/check
    path('parkinglist/check', views.check_car, name='check'),
    path('parkinglist/check/', views.check_car, name='check'),
    # ex: /parkinglist/records/1
    path('parkinglist/records/<int:page>', views.get_records, name='records'),
    path('parkinglist/records/<int:page>/', views.get_records, name='records'),
    # ex: /parkinglist/stats
    path('parkinglist/stats', views.statistics, name='stats'),
    path('parkinglist/stats/', views.statistics, name='stats'),
]