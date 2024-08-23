from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_label_values/', views.get_label_values, name='get_label_values'),
]