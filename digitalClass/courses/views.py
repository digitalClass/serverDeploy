from django.shortcuts import render,render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,Http404
from courses.models import Course, PPTfile, PPTslice
from users.models import User
from form import *

import datetime
# Create your views here.

@login_required
def profile(request):
    #profile, login required
    #authenticated -> get basic information from request.user
    #three part,request.user.user_role,only teacher's part now
    #if user is a teacher
	#get User object due to id
	#related_name='teacher'Course and User has a ManyToMany table
	#return course list
    #a teaching assistant
    #a student
    #not authenticated->redirect to somewhere
    if request.user.is_authenticated():
        user_email = request.user.email
        user_name = request.user.username
        user_id = request.user.id
        # te:Teacher;ta:TeachAssisstant;st:Student
        user_role = request.user.user_role
	if user_role == 'te':
	    teacher = User.objects.get(id=user.id)
	    courses_list = teacher.teacher.all()
	    return render_to_response('users/profile.html',{"user_name":user_name, "course_list":course_list})
	elif user_role == 'ta':
	    return HttpResponseRedirect('')
	 #Teaching Assistant's profile
	else:
	    #Student's profile
	    return HttpResponseRedirect('')
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
    if request.user.is_authenticated():
	if request.user.user_role == 'te':
	    if request.method == 'POST':
		form = CreateCourseForm(request.POST)
		if form.is_valid():
		    f = form.cleaned_data
		    now = datetime.datetime.now()
		    img = ''
		    user_id = request.user.id
		    c = Course.objects.create(introduce=f['course_date'], create_time=now, img_path=img, title=f['course_title'], course_id = f['course_id'])
		    u = User.objects.get(id=user_id)
		    c.teacher.add(u)
		    return HttePresponseRedirect('/accounts/profile/')
	    else:
		form = CreateCourseForm({'subject':'SUBJECT', 'course_id':'COUSRSE ID'})
    	    return render_to_response('create.html',{'form':form})
    return render_to_response("premissionDeniey.html")

def course_page(request, c_id):
    #course page
    #courses' information,ppt list are needed
    #Is_this_course_teacher 
    try:
	course_id = int(c_id)
    except ValueError:
	raise Http404()
    c = Course.objects.get(id=course_id)
    Is_this_course_teacher = False
    if is_authenticated():
	user_id = request.user.id
	u = c.teacher.filter(id=user_id)
	if u != []:
	    Is_this_course_teacher=True
    return render_to_response('course_page.html',{'course':c, 'Is_this_course_teacher':Is_this_course_teacher})



@login_required
def ppt_upload(request,c_id):
    #hang in the air(a ppt cut tool is needed.)
    #show uploaded files
    #uploaded_list = []
    #how to upload more than one file
    #where to redirect when uploaded
    if request.user.is_authenticated():
	if request.user.user_role == 'te':
	    if request.method == 'POST':
		form = UploadPPTForm(request.POST,request.FILES)
		if form.is_valid():
		    handle_upload_file(request.FILES['file'])
		    #return render_to_response()
		    return HttpResponse("Successful")
	    else:
		form = UploadPPTForm()
	    return render_to_response('ppt_upload.html',{'form':form})
    return render_to_response("premissionDeniey.html")

def handle_upload_file(f):
    file_name=""
    try:
	path = "media/editor" + time.strftime('/%Y/%m/%d/%H/%M/%S/')
	if not os.path.exist(path):
	    os.makedirs(path)
	    file_name = path + f.name
	    destination = open(file_name,'wb+')
	    for chunk in f.chunks():
		destination.write(chunk)
	    destination.close()
    except Exception, e:
	print e
    return file_name





