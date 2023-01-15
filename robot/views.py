from django.shortcuts import redirect
from django.views.generic import TemplateView


class DashboardView(TemplateView):
    template_name = "robot/dashboard.html"