#coding:utf-8
from __future__ import unicode_literals

from django.db import models
from users import models as users_models

class Course(models.Model):
	#采用内置自增id
	#id = models.IntegerField(primary_key=true)
	date = models.DateField()
	#课程创建时间
	create_time = models.DateTimeField(null=True)
	#the image path of this course showcases on courses list.
	img_path = models.CharField(max_length=256)
	#课程名称
	title = models.CharField(max_length=32,null=True)
	course_id = models.CharField(max_length=16)
	user_type = models.ForeignKey(users_models.User)
	def __unicode__(self):
		return self.title

class PPTfile(models.Model):
	#采用内置自增id
	#id = models.IntegerField(primary_key=true)
	date = models.DateField()
	#PPT上传时间
	upload_time = models.DateTimeField(null=True)
	#PPT名称
	title = models.CharField(max_length=32,null=True)
	course = models.ForeignKey(Course)

class PPTslice(models.Model):
	#采用内置自增id
	#id = models.IntegerField(primary_key=true)
	#index of a pptfile
	index = models.IntegerField()
	date = models.DateField()
	#the path of this slice of PPT
	img_path = models.CharField(max_length=256)
	pptfile = models.ForeignKey(PPTfile)

class Video(models.Model):
	#采用内置自增id
	#id = models.IntegerField(primary_key=true)
	#video index of a course
	index = models.IntegerField()
	date = models.DateField()
	#video上传时间
	upload_time = models.DateTimeField(null=True)
	#video名称
	title = models.CharField(max_length=32,null=True)
	video_path = models.CharField(max_length=256)
	course = models.ForeignKey(Course)













