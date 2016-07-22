#coding:utf-8
from django.shortcuts import render,render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,Http404,HttpResponse
from courses.models import Course, PPTfile, PPTslice
from users.models import User
from courses.form import *
from courses.filetype import *
from django.template import RequestContext
from digitalClass.utils import *
import os

import datetime
# Create your views here.

@login_required
def profile(request):
    #profile, login required
    #authenticated -> get basic information from request.user
    #three part,request.user.user_role,only teacher's part now
    #if user is a teacher
	#get User object according to id
	#related_name='teacher'Course and User has a ManyToMany table
	#return course list
    #a teaching assistant
    #a student
    #not authenticated->redirect to somewhere
    logined =False
    if request.user.is_authenticated():
        logined = True
        user_email = request.user.email
        user_name = request.user.username
        user_id = request.user.id
	useravatar = request.user.useravatar
        # te:Teacher;ta:TeachAssisstant;st:Student
        user_role = request.user.user_role
	try:
	    user = User.objects.get(id=user_id)
	except User.DoesNotExist:
	    return HttpResponse('something wrong!')

	if user_role == 'te':
	    course_list = user.teacher.all()
	elif user_role == 'ta':
	    return HttpResponseRedirect('')
	 #Teaching Assistant's profile
	else:
	    #Student's profile
	    course_list = user.subscribed_user.all()
        return render_to_response('users/profile.html',{"logined":logined,"user_name":user_name,"user_id":user_id,"user_role":user_role,"useravatar":useravatar, "course_list":course_list})
    return render_to_response("premissionDeniey.html")

@login_required
def create_course(request):
    #authenticated
    #is a teacher?
    #method = POST?
    #CreateCourseForm
    #is it valid?
    #a default image path is needed
    #has priority
	#timing
	#introduce
	#img_path
	#user_id
	#Course.save()
	#add Course.teacher
    #else -> redirect
    logined = False
    if request.user.is_authenticated():
        logined = True
	if request.user.user_role == 'te':
	    if request.method == 'POST':
		form = CreateCourseForm(request.POST)
		if form.is_valid():
		    f = form.cleaned_data
		    now = datetime.datetime.now()
		    img = ''
		    user_id = request.user.id
		    course = Course.objects.create(introduce=f['course_data'], create_time=now, img_path=img, title=f['course_title'], course_id = f['course_id'])
		    u = User.objects.get(id=user_id)
		    course.teacher.add(u)
		    return HttpResponseRedirect('/accounts/profile/')
	    else:
		form = CreateCourseForm({'subject':'SUBJECT', 'course_id':'COUSRSE ID'})
            return render_to_response('create.html',{'form':form,"logined":logined,"user_name":request.user.username},context_instance=RequestContext(request))
    return render_to_response("premissionDeniey.html")

@login_required
def course_edit(request, c_id):
    try:
	course_id = int(c_id)
    except ValueError:
	raise HttpResponse('Please input correct CourseID ')
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
	return HttpResponse('Course does not exist')
    if request.user.is_authenticated():
	teacher = course.teacher.filter(id = request.user.id)
	if teacher:
	    if request.method == 'POST':
		form = EditCourseForm(request.POST)
		if form.is_valid():
		    f = form.cleaned_data
		    course.title = f['course_title']
		    course.introduce = f['course_data']
		    course.course_id = f['course_id']
		    course.save()
		    return HttpResponseRedirect('/accounts/profile/')
	    else:
		form = EditCourseForm({'course_title':course.title, 'course_id':course.course_id, 'course_data':course.introduce})
    	    return render_to_response('create.html',{'form':form},context_instance=RequestContext(request))
    return HttpResponse('You aren\'t not the teacher of this course, you can\'t edit its infomation!')


def course_page(request, c_id):
    #course page
    #courses' information,ppt list are needed
    #Is_this_course_teacher
    try:
	course_id = int(c_id)
    except ValueError:
	raise Http404()
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
	return HttpResponse('Course does not exist')
    ppts = course.pptfile_set.all()
    Is_this_course_teacher = False
    Is_subscribed = False

    logined = False
    if request.user.is_authenticated():
        logined = True
	user_id = request.user.id
	u = course.teacher.filter(id=user_id)
	if u:
	    Is_this_course_teacher=True
	s = course.subscribed_user.filter(id=user_id)
	if s:
	    Is_subscribed = True
        if request.method == 'POST':
	    if request.POST['subscribed_status_changed']==u'True':
		if Is_subscribed:
		    course.subscribed_user.remove(request.user)
		    Is_subscribed = False
		else:
		    course.subscribed_user.add(request.user)
		    Is_subscribed = True
    else:
	if request.method == 'POST':
	    return HttpResponseRedirect('/accounts/login/')
    return render_to_response('course.html',{'logined':logined,'user_name':request.user.username,'user_role':request.user.user_role,'course':course, 'ppts':ppts, 'Is_this_course_teacher':Is_this_course_teacher, 'Is_subscribed':Is_subscribed},context_instance=RequestContext(request))
    #return render_to_response('course.html',{'course':course, 'ppts':ppts, 'Is_this_course_teacher':Is_this_course_teacher, 'Is_subscribed':Is_subscribed})

def course_test(request, c_id):
    #course page
    #courses' information,ppt list are needed
    #Is_this_course_teacher
    try:
	course_id = int(c_id)
    except ValueError:
	raise Http404()
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
	return HttpResponse('Course does not exist')
    ppts = course.pptfile_set.all()
    Is_this_course_teacher = False
    Is_subscribed = False

    if request.user.is_authenticated():
	user_id = request.user.id
	u = course.teacher.filter(id=user_id)
	if u:
	    Is_this_course_teacher=True
	s = course.subscribed_user.filter(id=user_id)
	if s:
	    Is_subscribed = True
        if request.method == 'POST':
	    if request.POST['subscribed_status_changed']==u'True':
		if Is_subscribed:
		    course.subscribed_user.remove(request.user)
		    Is_subscribed = False
		else:
		    course.subscribed_user.add(request.user)
		    Is_subscribed = True
    else:
	if request.method == 'POST':
	    return HttpResponseRedirect('/accounts/login/')
    return render_to_response('test_course/course_page.html',{'course':course, 'ppts':ppts, 'Is_this_course_teacher':Is_this_course_teacher, 'Is_subscribed':Is_subscribed},context_instance=RequestContext(request))




@login_required
def ppt_upload(request,c_id):
    #hang in the air(a ppt cut tool is needed.)
    #show uploaded files
    #uploaded_list = []
    #how to upload more than one file
    #where to redirect when uploaded
    try:
        course_id = int(c_id)
    except ValueError:
        raise Http404()
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return HttpResponse('Course does not exist')

    logined = False
    if request.user.is_authenticated():
        logined = True
	if request.user.user_role == 'te':
	    if request.method == 'POST':
		form = UploadPPTForm(request.POST,request.FILES)
		if form.is_valid():
		    f = form.cleaned_data
		    ppt_title = f['title']
		    upload_file = request.FILES['file']
		    If_ppt_existed = course.pptfile_set.filter(title=ppt_title)
		    if If_ppt_existed:
			return HttpResponse("A same named PPT has existed in this course!")
		    fname = handle_upload_file(upload_file,course_id,ppt_title)
		    ftype = filetype(fname)
		    if ftype != "PDF":
			#return HttpResponse(ftype)
		        return HttpResponse("You have to upload a pdf file.")
		    split_pdf(fname)
		    ppt = PPTfile.objects.create(title=ppt_title,upload_time=datetime.datetime.now(),introduce=f['data'],course_id=course_id)
		    #return render_to_response()
		    #return HttpResponse(fname)
		    if fname:
		        return HttpResponse("Successful.html")
	    else:
		form = UploadPPTForm()
            return render_to_response('test_course/ppt_upload.html',{'form':form,'logined':logined,'user_name':request.user.username}, context_instance=RequestContext(request))
    return render_to_response("premissionDeniey.html",{'logined':logined,'user_name':request.user.username})

def handle_upload_file(f,course_id,title):
    file_name=""
    try:
	#path = "media/editor" + datetime.time.strftime('/%Y/%m/%d/%H/%M/%S/')
	path = "media/digitalClass/ppts/%d/%s/"%(course_id,title)
	if not os.path.exists(path):
	    os.makedirs(path)
	file_name = path + f.name
	destination = open(file_name,'wb+')
	for chunk in f.chunks():
	    destination.write(chunk)
	    destination.close()
    except Exception, e:
	print e
    #return path
    return file_name 





