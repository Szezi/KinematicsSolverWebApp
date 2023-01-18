from django.db import models
from accounts.models import User


class Project(models.Model):
    admin = models.ManyToManyField(User, related_name='admin', null=False)
    name = models.CharField(default='New Project', max_length=200)
    description = models.CharField(max_length=250, null=True, blank=True, default='Project description')
    members = models.ManyToManyField(
        User, related_name='members', blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.name


class Robot(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=False)
    name = models.CharField(default='New task', max_length=200)
    description = models.CharField(max_length=100, null=True, blank=True, default='Task description')
    notes = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
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

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['created']



