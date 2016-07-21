from __future__ import unicode_literals

from django.db import models
from courses import models as courses_models
from users import models as users_models

class Feedback(models.Model):

	""" Definition of question posted in course notes"""
	date = models.DateTimeField()
	#in order to get feedback from AnonymousUser, set blank = True
	user = models.ForeignKey(users_models.User,null=True, blank=True)

	content = models.CharField(max_length=1024)

	def __unicode__(self):
		return self.content
