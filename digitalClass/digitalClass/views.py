#!coding:utf8
from django.http import HttpResponse
from django.template import Template,Context
from django.template.loader import get_template
from django.shortcuts import render_to_response
import MySQLdb
import datetime

def homepage(request):
    """print hello world on website

    :request: HttpRequest
    :returns: HttpResponse

    """
    return render_to_response("index.html")

def loginedHomepage(request):
    if request.user.is_authenticated:
        user_email = request.user.email
        user_last_login = request.user.last_login
        c = Context({"user_emil":user_email,"user_last_login":user_last_login})
    return render_to_response('users/profile.html',c)
