# core/urls.py
from django.urls import path
from .views import SchoolListView, school_create

urlpatterns = [
    path('schools/create/', school_create, name='school_create'),
    path('schools/', SchoolListView.as_view(), name='school_list'),
]