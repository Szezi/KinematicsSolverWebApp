import datetime
from django.db.models import Count
from rest_framework import generics, request, status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.utils import calculate_ik, calculate_fk


@api_view(['GET'])
def apiOverview(request):
    """
        An endpoint for overview of the api.
    """
    api_urls = {
        'Forward Kin Calc': '/api/fk-calc/<str:link1>_<str:link1_min>_<str:link1_max>/<str:link2>_<str:link2_min>_<str:link2_max>/<str:link3>_<str:link3_min>_<str:link3_max>/<str:link4>_<str:link4_min>_<str:link4_max>/<str:link5>_<str:link5_min>_<str:link5_max>/'
                            '<str:theta1>_<str:theta2>_<str:theta3>_<str:theta4>/',
        'Forward Kin Calc_ex': '/api/fk-calc/118_-80_80/150_5_175/150_-115_55/54_-85_85/0_0_0/0_90_0_0/',
        'Inverse Kin Calc': '/api/ik-calc/<str:link1>_<str:link1_min>_<str:link1_max>/<str:link2>_<str:link2_min>_<str:link2_max>/<str:link3>_<str:link3_min>_<str:link3_max>/<str:link4>_<str:link4_min>_<str:link4_max>/<str:link5>_<str:link5_min>_<str:link5_max>/'
                            '<str:x>_<str:y>_<str:z>_<str:alpha>/',
        'Inverse Kin Calc_ex': '/api/ik-calc/118_-80_80/150_5_175/150_-115_55/54_-85_85/0_0_0/0_0_472_90/',

    }

    return Response(api_urls)


class FkCalcAPIView(generics.ListAPIView):
    """
        An api endpoint for forward kinematics calculation.
    """
    permission_classes = (AllowAny,)
    # serializer_class = FkSerializer

    def get(self, request, *args, **kwargs):
        link1 = self.kwargs.get('link1')
        link1_min = self.kwargs.get('link1_min')
        link1_max = self.kwargs.get('link1_max')
        link2 = self.kwargs.get('link2')
        link2_min = self.kwargs.get('link2_min')
        link2_max = self.kwargs.get('link2_max')
        link3 = self.kwargs.get('link3')
        link3_min = self.kwargs.get('link3_min')
        link3_max = self.kwargs.get('link3_max')
        link4 = self.kwargs.get('link4')
        link4_min = self.kwargs.get('link4_min')
        link4_max = self.kwargs.get('link4_max')
        link5 = self.kwargs.get('link5')
        link5_min = self.kwargs.get('link5_min')
        link5_max = self.kwargs.get('link5_max')
        theta1 = self.kwargs.get('theta1')
        theta2 = self.kwargs.get('theta2')
        theta3 = self.kwargs.get('theta3')
        theta4 = self.kwargs.get('theta4')

        links = {
                    "link1": [int(link1), int(link1_min), int(link1_max)],
                    "link2": [int(link2), int(link2_min), int(link2_max)],
                    "link3": [int(link3), int(link3_min), int(link3_max)],
                    "link4": [int(link4), int(link4_min), int(link4_max)],
                    "link5": [int(link5), int(link5_min), int(link5_max)],
                }

        result = calculate_fk(links, float(theta1), float(theta2), float(theta3), float(theta4))
        x = float(result[0][1][3][0])
        y = float(result[0][1][3][1])
        z = float(result[0][1][3][2])
        alpha = float(result[0][0])
        status_calc = result[0][2]
        data = {
                    'link1': int(link1),
                    'link1_min': int(link1_min),
                    'link1_max': int(link1_max),
                    'link2': int(link2),
                    'link2_min': int(link2_min),
                    'link2_max': int(link2_max),
                    'link3': int(link3),
                    'link3_min': int(link3_min),
                    'link3_max': int(link3_max),
                    'link4': int(link4),
                    'link4_min': int(link4_min),
                    'link4_max': int(link4_max),
                    'link5': int(link5),
                    'link5_min': int(link5_min),
                    'link5_max': int(link5_max),
                    'theta1': float(theta1),
                    'theta2': float(theta2),
                    'theta3': float(theta3),
                    'theta4': float(theta4),

                    'status_calc': status_calc,
                    'x': x,
                    'y': y,
                    'z': z,
                    'alpha': alpha,
                }
        return Response(data, status=status.HTTP_200_OK)


class IkCalcAPIView(generics.ListAPIView):
    """
        An api endpoint for inverse kinematics calculation.
    """
    permission_classes = (AllowAny,)
    # serializer_class = IkSerializer

    def get(self, request, *args, **kwargs):
        link1 = self.kwargs.get('link1')
        link1_min = self.kwargs.get('link1_min')
        link1_max = self.kwargs.get('link1_max')
        link2 = self.kwargs.get('link2')
        link2_min = self.kwargs.get('link2_min')
        link2_max = self.kwargs.get('link2_max')
        link3 = self.kwargs.get('link3')
        link3_min = self.kwargs.get('link3_min')
        link3_max = self.kwargs.get('link3_max')
        link4 = self.kwargs.get('link4')
        link4_min = self.kwargs.get('link4_min')
        link4_max = self.kwargs.get('link4_max')
        link5 = self.kwargs.get('link5')
        link5_min = self.kwargs.get('link5_min')
        link5_max = self.kwargs.get('link5_max')
        x = self.kwargs.get('x')
        y = self.kwargs.get('y')
        z = self.kwargs.get('z')
        alpha = self.kwargs.get('alpha')

        links = {
                    "link1": [int(link1), int(link1_min), int(link1_max)],
                    "link2": [int(link2), int(link2_min), int(link2_max)],
                    "link3": [int(link3), int(link3_min), int(link3_max)],
                    "link4": [int(link4), int(link4_min), int(link4_max)],
                    "link5": [int(link5), int(link5_min), int(link5_max)],
                }

        result = calculate_ik(links, int(x), int(y), int(z), int(alpha))
        request.data['theta1'] = result[0][0][0]
        #         request.data['theta2'] = result[0][0][1]
        #         request.data['theta3'] = result[0][0][2]
        #         request.data['theta4'] = result[0][0][3]
        #         request.data['theta11'] = result[1][0][0]
        #         request.data['theta22'] = result[1][0][1]
        #         request.data['theta33'] = result[1][0][2]
        #         request.data['theta44'] = result[1][0][3]
        theta1 = float(result[0][0][0])
        theta2 = float(result[0][0][1])
        theta3 = float(result[0][0][2])
        theta4 = float(result[0][0][3])
        theta11 = float(result[1][0][0])
        theta22 = float(result[1][0][1])
        theta33 = float(result[1][0][2])
        theta44 = float(result[1][0][3])
        status_config1 = result[0][1]
        status_config2 = result[1][1]
        data = {
                    'link1': int(link1),
                    'link1_min': int(link1_min),
                    'link1_max': int(link1_max),
                    'link2': int(link2),
                    'link2_min': int(link2_min),
                    'link2_max': int(link2_max),
                    'link3': int(link3),
                    'link3_min': int(link3_min),
                    'link3_max': int(link3_max),
                    'link4': int(link4),
                    'link4_min': int(link4_min),
                    'link4_max': int(link4_max),
                    'link5': int(link5),
                    'link5_min': int(link5_min),
                    'link5_max': int(link5_max),
                    'x': x,
                    'y': y,
                    'z': z,
                    'alpha': alpha,

                    'Config1': status_config1,
                    'theta1': float(theta1),
                    'theta2': float(theta2),
                    'theta3': float(theta3),
                    'theta4': float(theta4),
                    'Config2': status_config2,
                    'theta11': float(theta11),
                    'theta22': float(theta22),
                    'theta33': float(theta33),
                    'theta44': float(theta44),

                }
        return Response(data, status=status.HTTP_200_OK)


