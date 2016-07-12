#coding:utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User2(models.Model):
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=16)
    password = models.CharField(max_length=32)
    email = models.EmailField()
    create_time = models.DateTimeField()
    gender = models.BooleanField()
    user_type = models.IntegerField()
    portait = models.URLField()
    def __unicode__(self):
        return self.user_name

class Question(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    def __unicode__(self):
        return self.name

class Course(models.Model):

    """Docstring for Book. """
    title = models.CharField(max_length=100)
    user_id = models.ForeignKey(User2)
    publication_date = models.DateField()
    categroy = models.IntegerField()
    def __unicode__(self):
        return self.title

class Answer(models.Model):
    content = models.CharField(max_length=1024)
