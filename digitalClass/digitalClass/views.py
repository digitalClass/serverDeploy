from django.http import HttpResponse
from django.template import Template,Context
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.http import HttpResponse
import MySQLdb
import datetime

def hello(request):
    """print hello world on website

    :request: HttpRequest
    :returns: HttpResponse

    """
    return HttpResponse("hello world")

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

def book_list(request):
    """TODO: Docstring for book_list.

    :request: TODO
    :returns: TODO

    """
    db = MySQLdb.connect(user='root',db='users',passwd='1234',host='localhost')
    cursor = db.cursor()
    cursor.execute('SELECT name FROM books ORDER BY name')
    names = [row[0] for row in cursor.fetchall()]
    db.close()
    return render_to_response('book_list.html',{'names':names})
