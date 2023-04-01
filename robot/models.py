from django.db import models
from django.db.models.functions import datetime
from django.urls import reverse
from django.utils import timezone

from accounts.models import User


class Project(models.Model):
    admin = models.ManyToManyField(User, related_name='admin', null=False)
    name = models.CharField(default='New Project', max_length=50)
    description = models.CharField(max_length=250, null=True, blank=True, default='Project description')
    members = models.ManyToManyField(
        User, related_name='members', blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.name


class Robot(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='robots', null=False)
    name = models.CharField(default='New robot', max_length=50)
    description = models.CharField(max_length=100, null=True, blank=True, default='Robot description')
    notes = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    link1 = models.IntegerField(null=True, blank=True, default=118)
    link2 = models.IntegerField(null=True, blank=True, default=150)
    link3 = models.IntegerField(null=True, blank=True, default=150)
    link4 = models.IntegerField(null=True, blank=True, default=0)
    link5 = models.IntegerField(null=True, blank=True, default=54)
    link1_min = models.IntegerField(null=True, blank=True, default=-80)
    link2_min = models.IntegerField(null=True, blank=True, default=5)
    link3_min = models.IntegerField(null=True, blank=True, default=-115)
    link4_min = models.IntegerField(null=True, blank=True, default=-85)
    link5_min = models.IntegerField(null=True, blank=True, default=0)
    link1_max = models.IntegerField(null=True, blank=True, default=80)
    link2_max = models.IntegerField(null=True, blank=True, default=175)
    link3_max = models.IntegerField(null=True, blank=True, default=55)
    link4_max = models.IntegerField(null=True, blank=True, default=85)
    link5_max = models.IntegerField(null=True, blank=True, default=0)

    def get_absolute_url(self):
        return reverse('robot-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created']


class ForwardKinematics(models.Model):
    Robot = models.OneToOneField(Robot, on_delete=models.CASCADE, related_name='fk_calc', null=False)
    name = models.CharField(default='FK Calculation', max_length=50)
    notes = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(null=True, blank=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    status = models.BooleanField(null=True, blank=True, default=False)
    theta1 = models.FloatField(null=True, blank=True, default=0.0)
    theta2 = models.FloatField(null=True, blank=True, default=0.0)
    theta3 = models.FloatField(null=True, blank=True, default=0.0)
    theta4 = models.FloatField(null=True, blank=True, default=0.0)
    x = models.FloatField(null=True, blank=True, default=0.0)
    y = models.FloatField(null=True, blank=True, default=0.0)
    z = models.FloatField(null=True, blank=True, default=0.0)
    alpha = models.FloatField(null=True, blank=True, default=0.0)

    def get_absolute_url(self):
        return reverse('fk-update', kwargs={'pk': self.pk})

    def __str__(self):
        return self.Robot.name


class InverseKinematics(models.Model):
    Robot = models.OneToOneField(Robot, on_delete=models.CASCADE, related_name='ik_calc', null=False)
    name = models.CharField(default='IK Calculation', max_length=50)
    notes = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(null=True, blank=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    status = models.BooleanField(null=True, blank=True, default=False)
    x = models.IntegerField(null=True, blank=True, default=0)
    y = models.IntegerField(null=True, blank=True, default=0)
    z = models.IntegerField(null=True, blank=True, default=0)
    alpha = models.IntegerField(null=True, blank=True, default=0)
    theta1 = models.FloatField(null=True, blank=True, default=0.0)
    theta2 = models.FloatField(null=True, blank=True, default=0.0)
    theta3 = models.FloatField(null=True, blank=True, default=0.0)
    theta4 = models.FloatField(null=True, blank=True, default=0.0)
    theta11 = models.FloatField(null=True, blank=True, default=0.0)
    theta22 = models.FloatField(null=True, blank=True, default=0.0)
    theta33 = models.FloatField(null=True, blank=True, default=0.0)
    theta44 = models.FloatField(null=True, blank=True, default=0.0)

    def get_absolute_url(self):
        return reverse('ik-update', kwargs={'pk': self.pk})

    def __str__(self):
        return self.Robot.name