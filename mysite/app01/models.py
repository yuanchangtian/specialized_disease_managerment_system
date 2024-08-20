#coding=utf-8
from __future__ import unicode_literals
from django.contrib import admin
from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField()
    is_changed = models.BooleanField(default=True)
    def __unicode__(self):
        return self.username
    def __str__(self):
        return self.username
