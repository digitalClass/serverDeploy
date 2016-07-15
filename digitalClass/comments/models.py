from __future__ import unicode_literals

from django.db import models
from courses import models as courses_models
from users import models as users_models

class Question(models.Model):

	""" Definition of question posted in course notes"""
	date = models.DateField()
	user = models.ForeignKey(users_models.User,null=True)
	course = models.ForeignKey(courses_models.Course,null=True)
	ppt_slice = models.ForeignKey(courses_models.PPTslice, null=True)
	content = models.CharField(max_length=1024)
	num_vote = models.IntegerField()

	def __unicode__(self):
		return self.content


class Answer(models.Model):

	""" Definition of answer posted in course notes"""
	date = models.DateField()
	user = models.ForeignKey(users_models.User,null=True)
	course = models.ForeignKey(courses_models.Course,null=True)
	question = models.ForeignKey(Question, null=True)
	user_role = models.CharField(max_length=2, null=True)
	content = models.CharField(max_length=1024)
	num_vote = models.IntegerField()

	def __unicode__(self):
		return self.content


class Question_Comment(models.Model):

	""" Definition of comment on question posted in course notes"""
	date = models.DateField()
	question = models.ForeignKey(Question, null=True)
	user = models.ForeignKey(users_models.User,null=True)
	content = models.CharField(max_length=1024)

	def __unicode__(self):
		return self.content


class Answer_Comment(models.Model):

	""" Definition of comment on question posted in course notes"""
	date = models.DateField()
	answer = models.ForeignKey(Answer, null=True)
	user = models.ForeignKey(users_models.User, null=True)
	content = models.CharField(max_length=1024)

	def __unicode__(self):
		return self.content

