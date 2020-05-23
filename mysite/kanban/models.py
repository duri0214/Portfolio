"""models.py"""
from django.contrib.auth.models import User
from django.db import models

class List(models.Model):
    """List"""
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
        
class Card(models.Model):
    """Card"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    list = models.ForeignKey(List, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
