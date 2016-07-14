#coding:utf-8
from __future__ import unicode_literals

from django.db import models
import peoples.models as peoples_models

class Course(models.Model):
	date = models.DateField()
	#the image path of this course showcases on courses list.
	img_path = models.CharField(max_length=256)
	course_id = models.CharField(max_length=16)
	user_type = models.ForeignKey(peoples_models.User)

class PPTfile(models.Model):
	date = models.DateField()
	course = models.ForeignKey(Course)

class PPTslice(models.Model):
	#index of a pptfile
	index = models.IntegerField(max_length=512)
	date = models.DateField()
	#the path of this slice of PPT
	img_path = models.CharField(max_length=256)
	pptfile = models.ForeignKey(PPTfile)

class Video(models.Model):
	#video index of a course
	index = models.IntegerField(max_length=64)
	date = models.DateField()
	video_path = models.CharField(max_length=256)
	course = models.ForeignKey(Course)













