#coding:utf-8

from celery.task import task
from digitalClass.utils import *

@task()
def split_pdf_background(name):
    split_pdf(name)
    




