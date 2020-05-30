"""models.py"""
from django.contrib.auth import get_user_model
from django.db import models

class List(models.Model):
    """List"""
    title = models.CharField(max_length=200)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Card(models.Model):
    """Card"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    list = models.ForeignKey(List, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
