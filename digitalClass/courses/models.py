#coding:utf-8
from __future__ import unicode_literals

from django.db import models
from users import models as users_models

class Course(models.Model):
	#采用内置自增id
	#id = models.IntegerField(primary_key=true)
	#课程简介
	introduce = models.CharField(max_length=256,null=True)
	#课程创建时间
	create_time = models.DateTimeField()
	#the image path of this course showcases on courses list.
	img_path = models.CharField(max_length=256)
	#课程名称
	title = models.CharField(max_length=32)
	course_id = models.CharField(max_length=16, null=True)
	#课程老师
	teacher = models.ManyToManyField(users_models.User,related_name="teacher")
	#课程助教
	teaching_assitant = models.ManyToManyField(users_models.User, related_name="teaching_assistant")
	def __str__(self):
	    return self.title
	class Meta:
	    ordering = ['title']


class PPTfile(models.Model):
	#采用内置自增id
	#id = models.IntegerField(primary_key=true)
	introduce = models.CharField(max_length=256,null=True)
	#PPT上传时间
	upload_time = models.DateTimeField()
	#PPT名称
	title = models.CharField(max_length=32)
	course = models.ForeignKey(Course)
	def __str__(self):
	    return self.title
	class Meta:
	    ordering = ['title']

class PPTslice(models.Model):
	#采用内置自增id
	#id = models.IntegerField(primary_key=true)
	#index of a pptfile
	index = models.IntegerField()
	upload_time = models.DateTimeField()
	#the path of this slice of PPT
	img_path = models.CharField(max_length=256)
	pptfile = models.ForeignKey(PPTfile)
	def __str__(self):
	    return self.index
	class Meta:
	    ordering = ['index']

class Video(models.Model):
	#采用内置自增id
	#id = models.IntegerField(primary_key=true)
	#video index of a course
	index = models.IntegerField()
	introduce = models.CharField(max_length=256,null=True)
	#video上传时间
	upload_time = models.DateTimeField()
	#video名称
	title = models.CharField(max_length=32)
	video_path = models.CharField(max_length=256)
	course = models.ForeignKey(Course)
	def __str__(self):
	    return self.title
	class Meta:
	    ordering = ['title']



