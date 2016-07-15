from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from courses.models import Course, PPTfile, PPTslice
from users.models import User
from forms import *

import datetime
# Create your views here.

@login_required
def profile(request):
    if request.user.is_authenticated():
        user_email = request.user.email
        user_name = request.user.username
        user_id = request.user.id
        # te:Teacher;ta:TeachAssisstant;st:Student
        user_role = request.user.user_role
	if user_role == 'te':
	    teacher = User.objects.get(id=user.id)
	    courses_list = teacher.courses_set.all()
	    return render_to_response('users/profile.html',{"user_name":user_name, "course_list":course_list})
	elif user_role == 'ta':
	    #Teaching Assistant's profile
	else :
	    #Student's profile
    return HttpResponseRedirect('')

@login_required
def create_course(request):
    #errors = []
    if request.user.is_authenticated():
	if request.user.user_role == 'te':
	    if request.method == 'POST':
		form = CreateCourseForm(request.POST)
		if form.is_valid():
		    now = datetime.datetime.now()
		    #这里需要一个默认的图片地址，在未上传ppt时显示
		    img = ''
		    #不知道user_type 是什么
		    user_id = request.user.id
		    c = Course(date=form.course_date, create_time=now, img_path=img, title=form.course_title, course_id = form.course_id, user_type=user_id)
		    c.save()
		    #暂时跳转的是个人主页，等课程写好了再改成课程主页
		    return HttePresponseRedirect('/accounts/profile')
		else:
		    #表单无效，设置初始值重新回到本页面，提示错误信息
	    else:
		form = CreateCourseForm('subject': 'SUBJECT', 'course_id':'COUSRSE ID')
    return HttpResponseRedirect('')

@login_required
def course_page(request, c_id):
    #已有课程的课程页面
    #调用课程信息、课程PPT列表，有一个上传PPT的link跳转到上传页面

@login_required
def ppt_upload(request,c_id):
    #可能需要填写一个表单
    #POST方法
    #后台需要调用ppt切分工具





