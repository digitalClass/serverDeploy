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
        user_name = request.user.username
    return render_to_response('users/profile.html',{"user_name":user_name,})
