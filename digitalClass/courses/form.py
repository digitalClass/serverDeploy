#coding:utf-8
from django import forms

class CreateCourseForm(forms.Form):
    course_title = forms.CharField(max_length=32,label='课程名称')
    course_id = forms.CharField(max_length=16,label='课程编号')
    course_teacher = forms.CharField(max_length=16,label='任课老师')
    course_data = forms.CharField(widget=forms.Textarea,label='课程简介')

class UploadPPTForm(forms.Form):
    title = forms.CharField(max_length=50,label='课件名称')
    file = forms.FileField(label='上传文件')	
    data = forms.CharField(widget=forms.Textarea,label='PPT简介')


class EditCourseForm(forms.Form):
    course_title = forms.CharField(max_length=32,label='课程名称')
    course_id = forms.CharField(max_length=16,label='课程编号')
    course_teacher = forms.CharField(max_length=16,label='任课老师')
    course_data = forms.CharField(widget=forms.Textarea,label='课程简介')



