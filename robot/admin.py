from django.contrib import admin
from .models import Project, Robot, ForwardKinematics, InverseKinematics
# Register your models here.
admin.site.register(Project)
admin.site.register(Robot)
admin.site.register(ForwardKinematics)
admin.site.register(InverseKinematics)

