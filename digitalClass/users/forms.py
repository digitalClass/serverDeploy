#!coding:utf8
from __future__ import unicode_literals
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _
from django.db import models

from .conf import settings
from .fields import HoneyPotField, PasswordField, UsersEmailField


class UserCreationForm(forms.ModelForm):

    error_messages = {
        'duplicate_email': _('邮件地址已被注册！'),
        'password_mismatch': _('两次密码不一致！'),
        'student_number':_('不是有效的科大学号！')
    }

    username = models.CharField(max_length=30)
    student_id = models.CharField(max_length=11)
    gender = models.CharField(max_length=1)
    email = UsersEmailField(label=_('电子邮件'), max_length=255)
    USER_ROLE=(('st','学生'),('te','老师'),('ta','助教'),)
    user_role = models.CharField(max_length=2)
    password1 = PasswordField(label=_('密码'))
    password2 = PasswordField(
        label=_('重复密码'),
        help_text=_(''))
    useravatar = models.FileField(),

    class Meta:
        model = get_user_model()
        fields = ('username','email','student_id','gender','user_role','useravatar',)

    def clean_email(self):

        # Since User.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data['email']
        try:
            get_user_model()._default_manager.get(email=email)
        except get_user_model().DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email',
        )

    def clean_password2(self):

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = not settings.USERS_VERIFY_EMAIL
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField(label=_('Password'), help_text=_(
        '我们不会存储密码明文, 所以无法看到您的密码 '
        '但你可以<a href=\"password/\">在此</a>修改您的密码.'))

    class Meta:
        model = get_user_model()
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        return self.initial['password']

class RegistrationForm(UserCreationForm):
    error_css_class = 'error'
    required_css_class = 'required'


class RegistrationFormTermsOfService(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which adds a required checkbox
    for agreeing to a site's Terms of Service.

    """
    tos = forms.BooleanField(
        label=_('I have read and agree to the Terms of Service'),
        widget=forms.CheckboxInput,
        error_messages={
            'required': _('You must agree to the terms to register')
        })


class RegistrationFormHoneypot(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which adds a honeypot field
    for Spam Prevention

    """
    accept_terms = HoneyPotField()

class EditForm(forms.ModelForm):

    username = models.CharField(max_length=30)
    student_id = models.CharField(max_length=11)
    gender = models.CharField(max_length=1)
    user_role = models.CharField(max_length=2)
    useravatar = models.ImageField(max_length=100),

    class Meta:
        model = get_user_model()
        fields = ('username','student_id','gender','user_role','useravatar',)

    def update(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = not settings.USERS_VERIFY_EMAIL
        if commit:
            user.save()
        return user
