from django.urls import path, include
from .views import Index

urlpatterns = [
    path('index', Index.as_view(), name='index')
]