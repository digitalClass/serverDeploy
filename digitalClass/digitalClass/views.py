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

def days_ahead(request, offset):
    """print offset days ahead current_datetime

    :request: TODO
    :offset: TODO
    :returns: TODO

    """
    try:
        days_offset = int(offset)
    except ValueError as e:
        raise Http404
    future_datetime = datetime.datetime.now() + datetime.timedelta(days=days_offset)
    return render_to_response('future_time.html',locals())
