#coding:utf-8

from celery.task import task
from digitalClass.utils import *

@task()
def split_pdf_background(pdf_path,course_id,ppt_title,create_img=False,save_dir=None):
    split_pdf(pdf_path,course_id,ppt_title,create_img,save_dir)
    




