from django.urls import path, include
from .views import Index, StationsListView, StationDetailView

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('stations/', StationsListView.as_view(), name='stations'),
    path('station/<str:uiccode>/', StationDetailView.as_view(), name='station')
]