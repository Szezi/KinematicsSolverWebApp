from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView, CustomRegisterView, UserDetail, UserUpdate, UserInfo, EmailChangeView, CustomPasswordChangeView

urlpatterns = [
    path('login', CustomLoginView.as_view(), name='login'),
    path('register', CustomRegisterView.as_view(), name='register'),
    path('logout', LogoutView.as_view(next_page='home'), name='logout'),
    path('profile-info/<int:pk>/', UserInfo.as_view(), name='profile-info'),
    path('profile-detail', UserDetail.as_view(), name='profile-detail'),
    path('profile-update', UserUpdate.as_view(), name='profile-update'),
    path('password-change', CustomPasswordChangeView.as_view(), name='password-change'),
    path('email-change', EmailChangeView.as_view(), name='email-change'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)