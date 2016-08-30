#!coding=utf8
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, resolve_url
from django.template.response import TemplateResponse
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import update_session_auth_hash
from django.views.decorators.debug import sensitive_post_parameters

from .compat import urlsafe_base64_decode
from .conf import settings
from .signals import user_activated, user_registered
from .utils import EmailActivationTokenGenerator, send_activation_email
from django.shortcuts import render_to_response

try:
    from django.contrib.sites.shortcuts import get_current_site
except ImportError:  # pragma: no cover
    from django.contrib.sites.models import get_current_site

from .models import User


if settings.USERS_SPAM_PROTECTION:  # pragma: no cover
    from .forms import RegistrationFormHoneypot as RegistrationForm
else:
    from .forms import RegistrationForm

from .forms import EditForm
from django.contrib.auth.forms import PasswordChangeForm


@csrf_protect
@never_cache
def register(request,
             template_name='users/registration_form.html',
             activation_email_template_name='users/activation_email.html',
             activation_email_subject_template_name='users/activation_email_subject.html',
             activation_email_html_template_name=None,
             registration_form=RegistrationForm,
             registered_user_redirect_to=None,
             post_registration_redirect=None,
             activation_from_email=None,
             current_app=None,
             extra_context=None):

    if registered_user_redirect_to is None:
        registered_user_redirect_to = getattr(settings, 'LOGIN_REDIRECT_URL')

    if request.user.is_authenticated():
            return redirect(registered_user_redirect_to)

    if not settings.USERS_REGISTRATION_OPEN:
        return redirect(reverse('users_registration_closed'))

    if post_registration_redirect is None:
        post_registration_redirect = reverse('users_registration_complete')

    if request.method == 'POST':
        form = registration_form(request.POST,request.FILES)
        if form.is_valid():
            if form.useravatar==None:
                print "yes"
                form.useravatar='avatar/default.png'
            # user.useravatar=SaveFile(request.FILES['useravatar'],'avatar/')
            user = form.save()
            if settings.USERS_AUTO_LOGIN_AFTER_REGISTRATION:
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
            elif not user.is_active and settings.USERS_VERIFY_EMAIL:
                opts = {
                    'user': user,
                    'request': request,
                    'from_email': activation_from_email,
                    'email_template': activation_email_template_name,
                    'subject_template': activation_email_subject_template_name,
                    'html_email_template': activation_email_html_template_name,
                }
                send_activation_email(**opts)
                user_registered.send(sender=user.__class__, request=request, user=user)
            return redirect(post_registration_redirect)
    else:
        form = registration_form()

    current_site = get_current_site(request)

    context = {
        'form': form,
        'site': current_site,
        'site_name': current_site.name,
        'title': _('Register'),
    }

    if extra_context is not None:  # pragma: no cover
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


def registration_closed(request,
                        template_name='users/registration_closed.html',
                        current_app=None,
                        extra_context=None):
    context = {
        'title': _('Registration closed'),
    }
    if extra_context is not None:  # pragma: no cover
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


def registration_complete(request,
                          template_name='users/registration_complete.html',
                          current_app=None,
                          extra_context=None):
    context = {
        'login_url': resolve_url(settings.LOGIN_URL),
        'title': _('Registration complete'),
    }
    if extra_context is not None:  # pragma: no cover
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


@never_cache
def activate(request,
             uidb64=None,
             token=None,
             template_name='users/activate.html',
             post_activation_redirect='/',
             current_app=None,
             extra_context=None):

    context = {
        'title': _('Account activation '),
    }

    if post_activation_redirect is None:
        post_activation_redirect = reverse('users_activation_complete')

    UserModel = get_user_model()
    assert uidb64 is not None and token is not None

    token_generator = EmailActivationTokenGenerator()

    try:
        uid = urlsafe_base64_decode(uidb64)
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.activate()
        user_activated.send(sender=user.__class__, request=request, user=user)
        if settings.USERS_AUTO_LOGIN_ON_ACTIVATION:
            user.backend = 'django.contrib.auth.backends.ModelBackend'  # todo - remove this hack
            login(request, user)
            messages.info(request, 'Thanks for registering. You are now logged in.')
        return redirect(post_activation_redirect)
    else:
        title = _('Email confirmation unsuccessful')
        context = {
            'title': title,
        }

    if extra_context is not None:  # pragma: no cover
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


def activation_complete(request,
                        template_name='users/activation_complete.html',
                        current_app=None,
                        extra_context=None):
    context = {
        'title': _('Activation complete'),
    }
    if extra_context is not None:  # pragma: no cover
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)

# def SaveFile(file,path='',fileName=''):
#     fileName=file._get_name() if fileName=='' else fileName
#     filePath=str(path)+str(fileName)
#     rootFilePath='%s%s' %(settings.MEDIA_ROOT,filePath)
#     fd=open(rootFilePath,'wb')
#     for chunk in file.chunks():
#         fd.write(chunk)
#     fd.close()
#     return filePath

@csrf_protect
def edit(request,template_name='users/edit.html',
        edit_form=EditForm,
        extra_context=None,
        current_app=None):
    """TODO: Docstring for edit.

    :request: TODO
    :template_name: TODO
    :returns: TODO

    """
    u = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = edit_form(request.POST, request.FILES, instance=u)
        if form.is_valid():
            form.save()
            return redirect("../profile/")
    else:
        INITIAL={'username':u.username,
                'student_id':u.student_id,
                'gender':u.gender,
                'user_role':u.user_role,
                'useravatar':u.useravatar,}
        form = edit_form(initial=INITIAL)

    current_site = get_current_site(request)
    if request.user.useravatar:
        useravatar = request.user.useravatar
    else:
        useravatar = 'avatar/default.png'
    context = {
        'logined': True,
        'form': form,
        'site': current_site,
        'site_name': current_site.name,
        'title': 'Modify personal information',
        'user_name': request.user.username,
        'useravatar': useravatar
    }

    if extra_context is not None:  # pragma: no cover
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)

@sensitive_post_parameters()
@csrf_protect
@login_required
def password_change(request,
                    template_name='registration/password_change_form.html',
                    post_change_redirect=None,
                    password_change_form=PasswordChangeForm,
                    extra_context=None):
    if post_change_redirect is None:
        post_change_redirect = reverse('password_change_done')
    else:
        post_change_redirect = resolve_url(post_change_redirect)
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Updating the password logs out all other sessions for the user
            # except the current one if
            # django.contrib.auth.middleware.SessionAuthenticationMiddleware
            # is enabled.
            update_session_auth_hash(request, form.user)
            # return redirect(post_change_redirect)
            return TemplateResponse(request, 'users/password_change_done.html', {'logined': True, 'user_name':request.user.username})
    else:
        form = password_change_form(user=request.user)
    if request.user.useravatar:
        useravatar = request.user.useravatar
    else:
        useravatar = 'avatar/default.png'
    context = {
        'form': form,
        'logined': True,
        'user_name': request.user.username,
        'useravatar': useravatar
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)


