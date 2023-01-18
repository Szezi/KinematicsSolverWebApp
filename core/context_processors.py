from django.http import HttpResponse
from robot.models import Project


def projects_list(request):
    projects = Project.objects.all()
    context = {'projects': projects}

    return (context)
