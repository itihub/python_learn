# 02_orms/django_orm/models.py

from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()

    def __str__(self):
        return self.name