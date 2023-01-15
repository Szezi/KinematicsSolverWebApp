from django.urls import path
from django.conf import settings
from .views import DashboardView

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name='dashboard'),
]
