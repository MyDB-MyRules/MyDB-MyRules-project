from django.urls import path
from . import views

urlpatterns = [
    path('', views.stocksview, name='stocksview'),
]