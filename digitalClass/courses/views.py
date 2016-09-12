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
import shutil


@login_required
def profile(request):
    '''
    生成个人主页
    已登陆用户访问个人主页，request中需要有用户登陆信息，方法需要登陆才可使用

    Args:
	request: request请求

    Returns:
	render_to_response(
	    'users/profile.html',
	    context,
	    context_instance=RequestContext(request))
	
        context = {
	    "logined":logined,
	    "user_name":user_name,
	    "user_id":user_id,
	    "user_role":user_role,
	    "useravatar":useravatar, 
	    "course_list":course_list,}

    '''	
    logined = True
    user = request.user
    user_email = user.email
    user_name = user.username
    user_id = user.id
    if user.useravatar:
	useravatar = user.useravatar
    else: useravatar = 'avatar/default.png'
    user_role = user.user_role
    # te:Teacher; ta:TeachAssistant; st:Student
    # Generate user's profile according to its user_role
    # course_list differs with user_role:
    #     teatcher: the course created by this user
    #     student: the course subscribed by this user
    # Teaching assistant's part has not been finished
    if user_role == 'te':
	course_list = user.teacher.filter(deleted=False)
	if request.method == 'POST': 
	    course_id = int(request.POST['course_id'])
	    course = Course.objects.get(id=course_id,deleted=False)
	    ppts = course.pptfile_set.all()
	    for ppt in ppts:
		delete_pptfile(ppt.id) #  Delete all of the ppts in this course
            course.deleted=True
            course.save()
	    return HttpResponseRedirect('')
    elif user_role == 'ta':
	return HttpResponseRedirect('')
    else:	#user_role == 'st'
	course_list = user.subscribed_user.filter(deleted=False)

    # This part is to deal with replies of user's questions, answers and 
    #     comments.
    context = {
	"logined":logined,
	"user_name":user_name,
	"user_id":user_id,
	"user_role":user_role,
	"useravatar":useravatar, 
	"course_list":course_list,}
    return render_to_response('users/profile.html',context,context_instance=RequestContext(request))

@login_required
def create_course(request):
    '''
    创建课程
    教师可以创建课程，教师身份才可以访问，其他身份会跳转至个人主页

    Args: 
        request
        request.POST
        request.user
        form = {
            course_title,
            course_id,
            course_teacher,
            course_data}

    Return: 
        render_to_response(
            'create.html',
            context,
            context_instance=RequestContext(request))

        context = {
            'form':form,
            'logined':logined,
            'user_name':user_name,}
    '''
    logined = True
    user_id = request.user.id
    user_name = request.user.username
    if request.user.user_role == 'te':
        if request.method == 'POST':
            form = CourseForm(request.POST)
            # if the form data is valid, create course
            # and return to profile
	    if form.is_valid():
	        f = form.cleaned_data
	        img = ''
	        course = Course.objects.create(
                    introduce=f['course_data'], 
                    img_path=img, 
                    title=f['course_title'], 
                    course_id = f['course_id'], 
                    teacher_name=f['course_teacher'])
	        u = User.objects.get(id=user_id)
	        course.teacher.add(u)
	        return HttpResponseRedirect('/accounts/profile/')
	else:
	    form = CourseForm()
        context = {
            'form':form,
            'logined':logined,
            'user_name':user_name,}
        return render_to_response('create.html',context,context_instance=RequestContext(request))
    return HttpResponseRedirect('/accounts/profile/') 

@login_required
def course_edit(request, c_id):
    try:
	course_id = int(c_id)
    except ValueError:
	raise HttpResponse('Please input correct CourseID ')
    try:
        course = Course.objects.get(id=course_id,deleted=False)
    except Course.DoesNotExist:
	return HttpResponse('Course does not exist')
    if request.user.is_authenticated():
	teacher = course.teacher.filter(id = request.user.id)
	if teacher:
	    if request.method == 'POST':
		form = CourseForm(request.POST)
		if form.is_valid():
		    f = form.cleaned_data
		    course.title = f['course_title']
		    course.introduce = f['course_data']
		    course.course_id = f['course_id']
		    course.teacher_name = f['course_teacher']
		    course.save()
		    return HttpResponseRedirect('/accounts/profile/')
	    else:
		form = CourseForm({'course_title':course.title, 'course_id':course.course_id, 'course_data':course.introduce})
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
        course = Course.objects.get(id=course_id,deleted=False)
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
	    if request.POST.get('subscribed_status_changed',''):
		if Is_subscribed:
		    course.subscribed_user.remove(request.user)
		    Is_subscribed = False
		else:
		    course.subscribed_user.add(request.user)
		    Is_subscribed = True
	    if request.POST.get('delete_ppt_id',''):
		delete_pptfile(request.POST['delete_ppt_id'])
		return HttpResponseRedirect('')
        context = {'logined':logined,
                'user_name':request.user.username,
                'user_role':request.user.user_role,
                'course':course,
                'ppts':ppts,
                'Is_this_course_teacher':Is_this_course_teacher,
                'Is_subscribed':Is_subscribed,}
	print request.POST
        return render_to_response('course.html',context,context_instance=RequestContext(request))
    else:
	if request.method == 'POST':
	    return HttpResponseRedirect('/accounts/login/')
    return render_to_response('course.html',{'course':course, 'ppts':ppts, 'Is_this_course_teacher':Is_this_course_teacher, 'Is_subscribed':Is_subscribed})

@login_required
def ppt_upload(request,c_id):
    #show uploaded files
    #uploaded_list = []
    #how to upload more than one file
    #where to redirect when uploaded
    try:
        course_id = int(c_id)
    except ValueError:
        raise Http404()
    try:
        course = Course.objects.get(id=course_id,deleted=False)
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
			#return HttpResponse("A same named PPT has existed in this course!")
			return render_to_response('test_course/ppt_upload_fail_crush.html',{'logined': request.user.is_authenticated(), 'user_name':request.user.username})
		    fname = handle_upload_file(upload_file,course_id,ppt_title)
		    ftype = filetype(fname)
		    if ftype != "PDF":
			#return HttpResponse(ftype)
		        #return HttpResponse("You have to upload a pdf file.")
			return render_to_response('test_course/ppt_upload_fail_type.html',{'logined': request.user.is_authenticated(), 'user_name':request.user.username})
		    ppt = PPTfile.objects.create(title=ppt_title,introduce=f['data'],source=fname,course_id=course_id)
		    if course.img_path=='':
		    	split_pdf.delay(fname,course_id,ppt_title,True)
		    	#split_pdf(fname,course_id,ppt_title,True)
		    else:
		    	split_pdf.delay(fname,course_id,ppt_title)
		    	#split_pdf(fname,course_id,ppt_title)
		    #name = os.path.split(fname)[1].split(".")[0]
		    #print name
		    #return HttpResponse(name)
		    #return render_to_response()
		    if fname:
		        #return HttpResponse("Successful.html")
			return render_to_response('test_course/ppt_upload_success.html',{'logined': request.user.is_authenticated(), 'user_name':request.user.username})
	    else:
		form = UploadPPTForm()
            return render_to_response('test_course/ppt_upload.html',{'form':form,'logined':logined,'user_name':request.user.username}, context_instance=RequestContext(request))
    return render_to_response("premissionDeniey.html",{'logined':logined,'user_name':request.user.username})

def handle_upload_file(f,course_id,title):
    file_name=""
    try:
	#path = os.path.join('media','digitalClass','ppts',course_id,title)
	#print 'path:',path
	path = "/media/digitalClass/ppts/%d/%s/"%(course_id,title)
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


def delete_pptfile(ppt_id):
    #从数据库和服务器中删除ppt及其对应的pptslice
    ppt = PPTfile.objects.get(id=int(ppt_id))
    if ppt:
	ppt.pptslice_set.all().delete()
    course_id = ppt.course.id
    title = ppt.title
    pptpath = "/media/digitalClass/ppts/%d/%s/"%(course_id,title)
    videopath = ""
    try:
	shutil.rmtree(pptpath)
	#shutil.rmtree(videopath)
	ppt.delete()
	print "{}\'s files have been deleted".format(title)	
    except Exception, e:
	print e
	


