#coding:utf-8
from django.shortcuts import render,render_to_response,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,Http404,HttpResponse
from courses.models import *
from users.models import User
from courses.form import UploadPPTForm
from courses.filetype import *
from django.template import RequestContext
from digitalClass.utils import *
import os
import shutil

from notifications.signals import notify

@login_required
def profile(request):
    '''
    生成个人主页
    已登陆用户访问个人主页，request中需要有用户登陆信息，方法需要登陆才可使用

    Args:
	request: request请求

    Returns:
	render(
            request
	    'users/profile.html',
	    context,

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
    return render(request,'users/profile.html',context)

@login_required
def create_course(request):
    '''
    创建课程
    教师可以创建课程，教师身份才可以访问，其他身份会跳转至个人主页

    Args:
        request
        request.POST
        request.user

    Return:
        response(
            request
            'create.html',
            context,

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
	        #f = form.cleaned_data
	        #img = ''
	        #course = Course.objects.create(
                    #introduce=f['course_data'],
                    #img_path=img,
                    #title=f['course_title'],
                    #course_id = f['course_id'],
                    #teacher_name=f['course_teacher'])
                course = form.save()
	        u = User.objects.get(id=user_id)
	        course.teacher.add(u)
	        return HttpResponseRedirect('/accounts/profile/')
	else:
	    form = CourseForm()
        context = {
            'form':form,
            'logined':logined,
            'user_name':user_name,}
        return render(request,'create.html',context)
    return HttpResponseRedirect('/accounts/profile/')

@login_required
def course_edit(request, c_id):
    '''
    课程编辑页面，实现对课程信息的编辑,会拒绝没有非创建该课程教师的访问
    
    Args:
        request
        request.POST = {
            'course_title':course_title,
            'course_data':course_date,
            'course_id':course_id,}

    Returns:
        HttpResponseRedirect('/accounts/profile/')

    context = {
        'form':form,
        'logined':logined,
        'user_name':user_name,}

    '''
    course = get_object_or_404(Course,id=int(c_id),deleted=False)
    teacher = course.teacher.filter(id = request.user.id)
    user_name = request.user.username
    logined = True
    if teacher:
        if request.method == 'POST':
            form = CourseForm(request.POST,instance=course)
	    if form.is_valid():
	        #f = form.cleaned_data
	        #course.title = f['course_title']
	        #course.introduce = f['course_data']
	        #course.course_id = f['course_id']
	        #course.teacher_name = f['course_teacher']
	        #course.save()
                form.save()
	        return HttpResponseRedirect('/accounts/profile/')
        else:
            form = CourseForm(
               # {'course_title':course.title, 
               # 'course_id':course.course_id, 
               # 'course_data':course.introduce,
               # 'course_teacher':course.teacher_name}
               instance = course)
        context = {
            'form':form,
            'logined':logined,
            'user_name':user_name,}
        return render(request,'create.html',context)
    return HttpResponse('You aren\'t not the teacher of this course, you can\'t edit its infomation!')


def course_page(request, c_id):
    '''
    课程页面
    每个课程有自己的页面，无需登陆即可访问，实现四种功能
    1.匿名访问课程页面
    Args:
        requset
        c_id 课程编号，由url取得，为字符串

    Return:
        render(request,'course.html',context)
        context = {
            'logined':logined,
            'course':course,
            'ppts':ppts,
            'Is_this_course_teacher':Is_this_course_teacher,
            'Is_subscribed':Is_subscribed,}

    2.登陆下访问课程页面
    Args:
        request
        request.user
        c_id

    Return:
        render(
            request
            'course.html',
            context)
        context = {'logined':logined,
                'user_name':request.user.username,
                'user_role':request.user.user_role,
                'course':course,
                'ppts':ppts,
                'Is_this_course_teacher':Is_this_course_teacher,
                'Is_subscribed':Is_subscribed,}

    3.学生订阅课程
    Args:
        request
        request.POST['subscribed_status_changed']
        request.user
        c_id

    Return:
        render(
            request
            'course.html',
            context)
        context = {'logined':logined,
                'user_name':request.user.username,
                'user_role':request.user.user_role,
                'course':course,
                'ppts':ppts,
                'Is_this_course_teacher':Is_this_course_teacher,
                'Is_subscribed':Is_subscribed,}

    4.开课老师删除课件或视频
    Args:
        request
        request.POST['delete_ppt_id']
        request.user
        c_id

    Return:
        return HttpResponseRedirect('')

    '''
    course = get_object_or_404(Course,id=int(c_id),deleted=False)
    ppts = course.pptfile_set.all()
    Is_this_course_teacher = False
    Is_subscribed = False
    logined = False

    if request.user.is_authenticated(): 
        logined = True
	user_id = request.user.id
        # To detemine if user is a teacher of this course
	u = course.teacher.filter(id=user_id) 
	if u:
	    Is_this_course_teacher=True
        # To detemine if the logined user is a subscribed user of this course
	s = course.subscribed_user.filter(id=user_id)
	if s:
	    Is_subscribed = True
        if request.method == 'POST':
            # To change the subscription status
	    if request.POST.get('subscribed_status_changed',''):
		if Is_subscribed:
		    course.subscribed_user.remove(request.user)
		    Is_subscribed = False
		else:
		    course.subscribed_user.add(request.user)
		    Is_subscribed = True
            # To delete one of its ppts or videos
            # Warning:This can only be applied by the creator
	    if request.POST.get('delete_ppt_id','') and Is_this_course_teacher:
		delete_pptfile(request.POST['delete_ppt_id'])
            elif request.POST.get('delete_video_id','') and Is_this_course_teacher:
                delete_video(request.POST['delete_video_id'])
            return HttpResponseRedirect('')
        context = {
                'logined':logined,
                'user_name':request.user.username,
                'user_role':request.user.user_role,
                'course':course,
                'ppts':ppts,
                'Is_this_course_teacher':Is_this_course_teacher,
                'Is_subscribed':Is_subscribed,}
	#print request.POST
        return render(request,'course.html',context)
    else:
        # reject POST method request for anonymous users
	if request.method == 'POST':
	    return HttpResponseRedirect('/accounts/login/')
    context = {
        'logined':logined,
        'course':course,
        'ppts':ppts,
        'Is_this_course_teacher':Is_this_course_teacher,
        'Is_subscribed':Is_subscribed,}
    return render(request,'course.html',context)

@login_required
def upload_ppt(request,c_id):
    '''
    '''
    # 
    course = get_object_or_404(Course,id=int(c_id),deleted=False)
    #ppts = course.pptfile_set.all()
    logined = True
    teacher = course.teacher.filter(id=request.user.id)
    if not teacher:
        HttpResponseRedirect('/accounts/profile')
    if request.method == 'POST':
        form = PPTfileForm(request.POST,request.FILES)
        if form.is_valid():
            #If_ppt_existed = course.pptfile_set.filter(title=ppt_title)
            ftype = filetype()
            ppt = form.save(commit=False)
            ppt.course = course.id
            ppt.save()
            


@login_required
def ppt_upload(request,c_id):
    #show uploaded files
    #uploaded_list = []
    #how to upload more than one file
    #where to redirect when uploaded
    course = get_object_or_404(Course,id=int(c_id),deleted=False)
    #ppts = course.pptfile_set.all()
    #logined = False
    #if request.user.is_authenticated():
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
		    fname = handle_upload_file(upload_file,course.id,ppt_title)
		    ftype = filetype(fname)
		    if ftype != "PDF":
			#return HttpResponse(ftype)
		        #return HttpResponse("You have to upload a pdf file.")
			return render_to_response('test_course/ppt_upload_fail_type.html',{'logined': request.user.is_authenticated(), 'user_name':request.user.username})
		    ppt = PPTfile.objects.create(title=ppt_title,introduce=f['data'],source=fname,course_id=course.id)
		    if course.img_path=='':
		    	#split_pdf.delay(fname,course_id,ppt_title,True)
		    	split_pdf(fname,course.id,ppt_title,True)
		    else:
		    	#split_pdf.delay(fname,course_id,ppt_title)
		    	split_pdf(fname,course.id,ppt_title)
		    #name = os.path.split(fname)[1].split(".")[0]
		    #print name
		    #return HttpResponse(name)
		    #return render_to_response()
		    if fname:
		        #return HttpResponse("Successful.html")
                        url = '/course/' + str(course.id)
                        recipient = request.user
                        notify.send(request.user, recipient=recipient, verb='上传了新课件:',
                            description=ppt_title, url=url)
			return render_to_response('test_course/ppt_upload_success.html',{'logined':request.user.is_authenticated(), 'user_name':request.user.username})
	    else:
		form = UploadPPTForm()
            context = {
                'form':form,
                'logined':logined,
                'user_name':request.user.username}
                
            return render(request,'test_course/ppt_upload.html',context)
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
    '''
    从数据库和服务器中删除ppt及其对应的pptslice模型及文件，删除时直接删除课件文件夹，会导致pdf源文件也被删除
    
    Args:
        ppt_id 要删除的ppt的id，可能为string数据或者int数据 
    '''
    # First, delete all slice model of this ppt
    # Second, get the path of this ppt
    # Third, delete all the file of ppt and slices
    ppt = get_object_or_404(PPTfile,id=int(ppt_id))
    ppt.pptslice_set.all().delete()
    pptpath = "/media/digitalClass/ppts/%d/%s/"%(ppt.course.id,ppt.title)
    try:
	shutil.rmtree(pptpath)
        if not os.path.exists(pptpath):
	    print "{}\'s files have been deleted".format(ppt.title)
	    ppt.delete()
    except Exception, e:
	print e

def delete_video(video_id):
    '''
    从数据库和服务器中删除video对应的模型及文件
    
    Args:
        video_id 要删除的video的id，可能为string数据或者int数据 
    '''
    # 
    video = get_object_or_404(Video,id=int(video_id))
    pptpath = "/media/digitalClass/video/%d/%s/"%(video.course_id,video.title)
    try:
	shutil.rmtree(pptpath)
        if not os.path.exists(pptpath):
	    print "{}\'s files have been deleted".format(video.title)
	    video.delete()
    except Exception, e:
	print e

