from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Question(models.Model):

	""" Definition of question posted in course notes"""
	id = models.IntegerField(primary_key=True)
	date = models.DateField()
	user_id = models.IntegerField()
	course_id = models.IntegerField()
	content = models.CharField(max_length=1024)
	num_vote = models.IntegerField()

	def __unicode__(self):
		return self.content


class Answer(models.Model):

	""" Definition of answer posted in course notes"""
	id = models.IntegerField(primary_key=True)
	date = models.DateField()
	user_id = models.IntegerField()
	course_id = models.IntegerField()
	user_type = models.IntegerField()
	content = models.CharField(max_length=1024)
	num_vote = models.IntegerField()

	def __unicode__(self):
		return self.content


class Question_Comment(models.Model):

	""" Definition of comment on question posted in course notes"""
	id = models.IntegerField(primary_key=True)
	date = models.DateField()
	question_id = models.IntegerField()
	user_id = models.IntegerField()
	content = models.CharField(max_length=1024)

	def __unicode__(self):
		return self.content


class Answer_Comment(models.Model):

	""" Definition of comment on question posted in course notes"""
	id = models.IntegerField(primary_key=True)
	date = models.DateField()
	answer_id = models.IntegerField()
	user_id = models.IntegerField()
	content = models.CharField(max_length=1024)

	def __unicode__(self):
		return self.content

