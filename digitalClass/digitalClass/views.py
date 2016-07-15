#!coding:utf8
from django.http import HttpResponseRedirect,HttpResponse
from django.template import Template,Context,loader
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import datetime

now = datetime.datetime.now()
def homepage(request):
    if not request.user.is_authenticated():
        return render_to_response("index.html")
    else:
        html = "<html><h1>need to be doen<h1><a href='accounts/logout'>注销</a></html>"
        return HttpResponse(html)

@login_required
def profile(request):
    if request.user.is_authenticated():
        user_email = request.user.email
        user_name = request.user.username
        user_id = request.user.id
        # te:Teacher;ta:TeachAssisstant;st:Student
        user_role = request.user.user_role
    return render_to_response('users/profile.html',{"user_name":user_name,})

def classroom(request):
    return render_to_response('player.html')

def create(request):
    return render_to_response('create.html')

# for logout quiet;
# but it seems doesn't work'
@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
