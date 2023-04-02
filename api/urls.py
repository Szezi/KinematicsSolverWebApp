from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import apiOverview, FkCalcAPIView, IkCalcAPIView

urlpatterns = [
    path('', apiOverview, name="api-overview"),
    path('fk-calc/<str:link1>_<str:link1_min>_<str:link1_max>/<str:link2>_<str:link2_min>_<str:link2_max>/<str:link3>_<str:link3_min>_<str:link3_max>/<str:link4>_<str:link4_min>_<str:link4_max>/<str:link5>_<str:link5_min>_<str:link5_max>/<str:theta1>_<str:theta2>_<str:theta3>_<str:theta4>/', FkCalcAPIView.as_view(), name='fk-calc'),
    path('ik-calc/<str:link1>_<str:link1_min>_<str:link1_max>/<str:link2>_<str:link2_min>_<str:link2_max>/<str:link3>_<str:link3_min>_<str:link3_max>/<str:link4>_<str:link4_min>_<str:link4_max>/<str:link5>_<str:link5_min>_<str:link5_max>/<str:x>_<str:y>_<str:z>_<str:alpha>/', IkCalcAPIView.as_view(), name='ik-calc'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
