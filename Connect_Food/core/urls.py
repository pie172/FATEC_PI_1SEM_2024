from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('doar/', views.doar_alimento, name='doar_alimento'),
    path('receber/', views.receber_alimento, name='receber_alimento'),
]
