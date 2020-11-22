from django.urls import path

from . import views

urlpatterns = [
    path('', views.main_func, name='main_func'),
]
