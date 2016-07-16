"""digitalClass URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.auth import urls
from digitalClass.views import *
from courses import views as courses_views

urlpatterns = [
    url(r'^$', homepage),
    url(r'^admin/', admin.site.urls),
# app users
    url(r'^accounts/logout$',logout_user),
    url(r'^accounts/', include('users.urls')),
    url(r'^accounts/profile/$', profile),
    url(r'^create/$', create, name="create_course"),
    url(r'^classroom/(\d+)/(\d+)/$',classroom),
]

urlpatterns += [
    url(r'^create_course/$', courses_views.create_course),
    url(r'^course_page/(\d+)/$', courses_views.course_page),
    url(r'ppt_upload/$', courses_views.ppt_upload),
]
