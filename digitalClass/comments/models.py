from __future__ import unicode_literals

from django.db import models
from courses import models as courses_model
from users import models as users_model
# Create your models here.
class Question(models.Model):

	""" Definition of question posted in course notes"""
	date = models.DateField()
	user = models.ForeignKey(users_model.User)
	course = models.ForeignKey(courses_model.Course)
	content = models.CharField(max_length=1024)
	num_vote = models.IntegerField()

	def __unicode__(self):
		return self.content


class Answer(models.Model):

	""" Definition of answer posted in course notes"""
	date = models.DateField()
	user = models.ForeignKey(users_model.User)
	course = models.ForeignKey(courses_model.Course)
	user_type = models.IntegerField()
	content = models.CharField(max_length=1024)
	num_vote = models.IntegerField()

	def __unicode__(self):
		return self.content


class Question_Comment(models.Model):

	""" Definition of comment on question posted in course notes"""
	date = models.DateField()
	question = models.IntegerField()
	user = models.ForeignKey(users_model.User)
	content = models.CharField(max_length=1024)

	def __unicode__(self):
		return self.content


class Answer_Comment(models.Model):

	""" Definition of comment on question posted in course notes"""
	date = models.DateField()
	answer = models.IntegerField()
	user = models.ForeignKey(users_model.User)
	content = models.CharField(max_length=1024)

	def __unicode__(self):
		return self.content

