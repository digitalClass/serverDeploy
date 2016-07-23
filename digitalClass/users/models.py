#!coding:utf8
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .conf import settings
from .managers import UserInheritanceManager, UserManager


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    USERS_AUTO_ACTIVATE = not settings.USERS_VERIFY_EMAIL

    email = models.EmailField(
            _('email address'), max_length=255, unique=True, db_index=True)
    is_staff = models.BooleanField(
            _('staff status'), default=False,
            help_text=_('Designates whether the user can log into this admin site.'))

    is_active = models.BooleanField(
            _('active'), default=USERS_AUTO_ACTIVATE,
            help_text=_('Designates whether this user should be treated as '
                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    username = models.CharField(_('用户名'),max_length=30, unique=True, null=True)
    student_id = models.CharField('学号或工号',max_length=30, null=True, blank=True)

    MALE = 'm'
    FEMALE = 'f'
    GENDER = ((MALE, '男'),(FEMALE,'女'),)
    gender = models.CharField('性别',
            max_length=1,
            choices=GENDER,
            default=MALE)

    user_type=models.ForeignKey(ContentType,null=True,editable=False)

    TEACHER='te'
    TA='ta'
    STUDENT='st'
    USER_ROLE=((TEACHER,'老师'),(TA,'助教'),(STUDENT,'学生'),)
    user_role=models.CharField(
            '类型',
            max_length=2,
            choices=USER_ROLE,
            default=STUDENT)
    useravatar = models.FileField('用户头像',upload_to="avatar",null = True, blank=True,)

    objects = UserInheritanceManager()
    base_objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        abstract = True

    def get_full_name(self):
        """ Return the email."""
        return self.email

    def get_short_name(self):
        """ Return the email."""
        return self.email

    def email_user(self, subject, message, from_email=None):
        """ Send an email to this User."""
        send_mail(subject, message, from_email, [self.email])

    def activate(self):
        self.is_active = True
        self.save()

    def save(self, *args, **kwargs):
        if not self.user_type_id:
            self.user_type = ContentType.objects.get_for_model(self, for_concrete_model=False)
        super(AbstractUser, self).save(*args, **kwargs)


class User(AbstractUser):

    """
    Concrete class of AbstractUser.
    Use this if you don't need to extend User.
    """

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
