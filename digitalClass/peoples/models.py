from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from users.models import User
# Create your models here.

class People(User):
    name = models.CharField(_('name'),max_length=30)

    class Meta:
        verbose_name = _('People')
        verbose_name_plural = _('Peoples')

