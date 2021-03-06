#coding:utf-8
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from users import models as users_models
from django.forms import ModelForm,Textarea
from django.core.exceptions import ValidationError
import gettext
from filetype import *

class Course(models.Model):
	introduce = models.CharField('课程简介',max_length=256,null=True)
	create_time = models.DateTimeField('课程创建时间',auto_now_add=True)
	img = models.ImageField('缩略图',upload_to='thumbnail/',null=True,blank=True)
	title = models.CharField('课程名称',max_length=32)
	course_id = models.CharField('课程编号',max_length=16, null=True)
	teacher_name = models.CharField('任课老师',max_length=16,default='')
	teacher = models.ManyToManyField(users_models.User,related_name="teacher")
	#课程助教
	teaching_assitant = models.ManyToManyField(users_models.User, related_name="teaching_assistant")
	#订阅该课程用户
	subscribed_user = models.ManyToManyField(users_models.User,related_name="subscribed_user")
	#是否删除
	deleted = models.BooleanField(default=False)
	def __str__(self):
	    return self.title
	class Meta:
	    ordering = ['create_time']

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['title','course_id','teacher_name','img','introduce']
        widgets = {
            'introduce':Textarea()}


def PPTfileUploadTo(instance,filename):
    return 'ppts/{}/{}/{}'.format(instance.course.id,instance.title,filename)

@python_2_unicode_compatible
class PPTfile(models.Model):
    introduce = models.CharField('课件简介',max_length=256,null=True)
    upload_time = models.DateTimeField('上传时间',auto_now_add=True)
    title = models.CharField('课件标题',max_length=32)
    #source = models.CharField('资源',max_length=256,default="")
    course = models.ForeignKey(Course)
    source = models.FileField('上传课件',upload_to=PPTfileUploadTo)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title']

class PPTfileForm(ModelForm):
    def clean_source(self):
        source = self.cleaned_data.get('source')
        ftype = filetype(source)
        if ftype != 'PDF':
            raise ValidationError(
                u'请上传PDF文件')
        return source
    class Meta:
        model = PPTfile
        fields = ['title','source','introduce']
        widgets = {
            'introduce':Textarea()}

class PPTslice(models.Model):
	index = models.IntegerField('相对位置',db_column='offset')
	upload_time = models.DateTimeField('上传时间',auto_now_add=True)
	img_path = models.CharField('图片',max_length=256)
	pptfile = models.ForeignKey(PPTfile)
	def __str__(self):
	    return self.index
	class Meta:
	    ordering = ['index']

class Video(models.Model):
	index = models.IntegerField('相对位置',db_column='offset')
	introduce = models.CharField('视频简介',max_length=256,null=True)
	upload_time = models.DateTimeField('上传时间',auto_now_add=True)
	title = models.CharField('视频标题',max_length=32)
	video_path = models.CharField('视频',max_length=256)
	course = models.ForeignKey(Course)
	def __str__(self):
	    return self.title
	class Meta:
	    ordering = ['title']



