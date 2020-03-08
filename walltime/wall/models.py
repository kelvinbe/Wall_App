from django.db import models
from django.contrib.auth.models import User


# Create your models here.
""" Message Model"""
class Message(models.Model):
    message = models.TextField(verbose_name=('New_Message'))
    author = models.ForeignKey(User, verbose_name=('Author'), related_name='author', on_delete=models.CASCADE)
    posted = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        ordering = ['posted']

