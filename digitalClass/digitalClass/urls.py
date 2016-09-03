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
from digitalClass import views as digitalClass_views
from django.conf import settings
from django.conf.urls import patterns
from courses import views as courses_views
from django.views.static import serve

urlpatterns = [
    url(r'^$', digitalClass_views.homepage),
    url(r'^admin/', admin.site.urls),
# app users
    url(r'^accounts/logout$',digitalClass_views.logout_user),
    url(r'^accounts/', include('users.urls')),
    #url(r'^accounts/profile/$', profile),
    #url(r'^create/$', create, name="create_course"),
    url(r'^addcomments/$', digitalClass_views.add_comments),
    url(r'^feedback/$', digitalClass_views.feedback),
    url(r'^thanks/$', digitalClass_views.thanks),
    url(r'^building/$', digitalClass_views.building),
    url(r'^classroom/(\w+)/([\w|\W]+)/(\-{0,1}\w+)/$',digitalClass_views.classroom),
    url(r'^addvote/$', digitalClass_views.add_vote),
    url(r'^page_change/$', digitalClass_views.page_change),
]

urlpatterns += [
    url(r'^create/$', courses_views.create_course),
    url(r'^course/(\d+)/$', courses_views.course_page),
    url(r'^accounts/profile/$', courses_views.profile),
    url(r'^course/(\d+)/ppt_upload/$', courses_views.ppt_upload),
    url(r'^course/(\d+)/edit/$', courses_views.course_edit),
]

#error routes
urlpatterns += [
    url(r'^404/$', digitalClass_views.page_404),
]

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += [
        url(r'^course_test/(\d+)/$', courses_views.course_test),
        url(r'^course_test/(\d+)/ppt_upload$', courses_views.ppt_upload),
]
    urlpatterns += [
	url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
	]

