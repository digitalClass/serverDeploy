#coding:utf-8
from __future__ import unicode_literals

from django.db import models
import users.models as users_models

class Course(models.Model):
	#采用内置自增id
	#id = models.IntegerField(primary_key=true)
	date = models.DateField()
	#课程创建时间
	create_time = models.DateTimeField()
	#the image path of this course showcases on courses list.
	img_path = models.CharField(max_length=256)
	#课程名称
	title = models.CharFiedl(max_length=32)
	course_id = models.CharField(max_length=16)
	user_type = models.ForeignKey(users_models.User)

class PPTfile(models.Model):
	#采用内置自增id
	#id = models.IntegerField(primary_key=true)
	date = models.DateField()
	#PPT上传时间
	upload_time = models.DateTimeField()
	#PPT名称
	title = models.CharFiedl(max_length=32)
	course = models.ForeignKey(Course)

class PPTslice(models.Model):
	#采用内置自增id
	#id = models.IntegerField(primary_key=true)
	#index of a pptfile
	index = models.IntegerField(max_length=512)
	date = models.DateField()
	#the path of this slice of PPT
	img_path = models.CharField(max_length=256)
	pptfile = models.ForeignKey(PPTfile)

class Video(models.Model):
	#采用内置自增id
	#id = models.IntegerField(primary_key=true)
	#video index of a course
	index = models.IntegerField(max_length=64)
	date = models.DateField()
	#video上传时间
	upload_time = models.DateTimeField()
	#video名称
	title = models.CharFiedl(max_length=32)
	video_path = models.CharField(max_length=256)
	course = models.ForeignKey(Course)













