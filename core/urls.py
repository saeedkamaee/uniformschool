# core/urls.py
from django.urls import path
from .views import school_create

urlpatterns = [
    path('schools/create/', school_create, name='school_create'),
]