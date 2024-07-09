from django.urls import path
from . import views

urlpatterns = [
    path('', views.grade_list, name='grade_list'),
    path('create/', views.grade_create, name='grade_create'),
    path('<int:pk>/edit/', views.grade_edit, name='grade_edit'),
]