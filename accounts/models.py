from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(
        max_length=15, blank=False, null=False, unique=True)
    email = models.EmailField(
        max_length=255, blank=False, null=False, unique=True)
    first_name = models.CharField(max_length=255, blank=False, null=True)
    last_name = models.CharField(max_length=255, blank=False, null=True)
    description = models.CharField(max_length=100, default='Users desc.')
    city = models.CharField(max_length=100, default='Unknown city')
    phoneNumber = models.IntegerField(default=555666333)
    bio = models.CharField(max_length=225, default='Users bio')
    avatar = models.ImageField(null=True, default="default-avatar")

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
