from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.
""" Message Model"""
class Message(models.Model):
    description = models.TextField(verbose_name=('New_Post'))
    author = models.ForeignKey('auth.User', related_name='description', on_delete=models.CASCADE, null=True)
    posted = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        ordering = ['posted']
