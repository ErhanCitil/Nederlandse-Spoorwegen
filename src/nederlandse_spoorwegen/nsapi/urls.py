from django.urls import path, include
from .views import Index, StationView, StationDetailView

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('stations/', StationView.as_view(), name='stations'),
    path('station/<str:uiccode>', StationDetailView.as_view(), name='station')
]