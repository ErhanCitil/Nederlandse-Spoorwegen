from django.urls import path, include
from .views import Index, StationView

urlpatterns = [
    path('index/', Index.as_view(), name='index'),
    path('stations/', StationView.as_view(), name='stations'),
]