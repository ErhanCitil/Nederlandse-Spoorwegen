from django.urls import path, include
from .views import Index, StationView, StationDetailView

urlpatterns = [
    path('index/', Index.as_view(), name='index'),
    path('stations/', StationView.as_view(), name='stations'),
    path('station/<str:name>/', StationDetailView.as_view(), name='station')
]