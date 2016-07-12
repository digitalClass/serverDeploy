from django.http import HttpResponse
from django.template import Template,Context
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.http import HttpResponse
import MySQLdb
import datetime

def homepage(request):
    """print hello world on website

    :request: HttpRequest
    :returns: HttpResponse

    """
    return render_to_response("index.html")

def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('current_datetime.html',{'current_datetime': now})

