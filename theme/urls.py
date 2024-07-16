from django.urls import path
from . import views

urlpatterns = [
    path('tailwind/', views.tailwind_demo, name='tailwind_demo'),
]