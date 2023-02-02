from django.urls import path
from django.conf import settings
from .views import DashboardView, ProjectCreate, ProjectDelete, ProjectUpdate, ProjectDetail, RobotCreate, RobotDelete, RobotUpdate, RobotDetail, FkCreate, FkUpdate, IkCreate, IkUpdate
from django.conf.urls.static import static

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name='dashboard'),

    path('project-create/', ProjectCreate.as_view(), name='project-create'),
    path('project-detail/<int:pk>/', ProjectDetail.as_view(), name='project-detail'),
    path('project-update/<int:pk>/', ProjectUpdate.as_view(), name='project-update'),
    path('project-delete/<int:pk>/', ProjectDelete.as_view(), name='project-delete'),

    path('robot-create/', RobotCreate.as_view(), name='robot-create'),
    path('robot-detail/<int:pk>/', RobotDetail.as_view(), name='robot-detail'),
    path('robot-update/<int:pk>/', RobotUpdate.as_view(), name='robot-update'),
    path('robot-delete/<int:pk>/', RobotDelete.as_view(), name='robot-delete'),

    path('fk-create/', FkCreate.as_view(), name='fk-create'),
    path('fk-update/<int:pk>/', FkUpdate.as_view(), name='fk-update'),

    path('ik-create/', IkCreate.as_view(), name='ik-create'),
    path('ik-update/<int:pk>/', IkUpdate.as_view(), name='ik-update'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)