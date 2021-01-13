from django.urls import path

from . import views

urlpatterns = [
    path('', views.main_func, name='main_view_func'),
    path('data-viz/', views.func_present_data, name='view_func_present_data'),
]
