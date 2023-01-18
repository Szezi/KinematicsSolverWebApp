from django.urls import path
from django.conf import settings
from .views import DashboardView, ProjectCreate, ProjectDelete, ProjectUpdate, ProjectDetail

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name='dashboard'),

    path('project-create/', ProjectCreate.as_view(), name='project-create'),
    path('project-detail/<int:pk>/', ProjectDetail.as_view(), name='project-detail'),
    path('project-update/<int:pk>/', ProjectUpdate.as_view(), name='project-update'),
    path('project-delete/<int:pk>/', ProjectDelete.as_view(), name='project-delete')
]
