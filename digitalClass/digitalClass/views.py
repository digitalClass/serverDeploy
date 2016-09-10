#!coding:utf8
from django.http import HttpResponseRedirect,HttpResponse
from django.template import Template,Context,loader, RequestContext
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import datetime
import json
import urllib
import math

from comments import models as comments_models
from comments import views as comments_views
from users import models as users_models
from courses import models as courses_models
from courses import views as courses_views
from digitalClass import models as digital_models
from django.core.mail import send_mail
from django_ajax.decorators import ajax

from users.models import User

now = datetime.datetime.now()
def homepage(request):
    # 不用登陆也能看到课程列表
    page_num = 12
    courses = courses_models.Course.objects.filter(deleted=False)
	#get number of total page, use ceil function to ensure correction
    total_page = int(math.ceil(float(courses.count()) / page_num))
    print('================total_page', total_page)
    if request.user.is_authenticated():
        username = request.user.username
        user_id = request.user.id
        # te:Teacher;ta:TeachAssisstant;st:Student
        user_role = request.user.user_role
        return render_to_response("index.html",{"logined":True,\
		'user_name':username,'user_id':user_id,'user_role':user_role,\
		"courses":courses[:page_num], 'curpage':1, 'total_page': total_page,\
		'page_num': page_num, 'page_num_list': range(1,total_page+1)})
    else:
        return render_to_response("index.html",{"logined": False,"courses":courses[:page_num],'curpage':1, 'total_page': total_page,'page_num': page_num, 'page_num_list': range(1, total_page+1)})
		

@login_required
def profile(request,
        template_name="users/profile.html"):
    if request.user.is_authenticated():
        username = request.user.username
        user_id = request.user.id
        useravatar = request.user.useravatar
        # te:Teacher;ta:TeachAssisstant;st:Student
        user_role = request.user.user_role
        c = Context({"username":username,"user_id":user_id,"user_role":user_role,"useravatar":useravatar,})
        t = get_template(template_name)
    # else:username="游客"
    # 若未登录而进入profile会跳到登录页面
    return HttpResponse(t.render(c))

def classroom(request, course_id, ppt_title, slice_index):
	try:
		course_id = int(course_id)
		slice_index= int(slice_index)
	except ValueError:
		return HttpResponseRedirect('/404/')
	if slice_index <= 0:
		return HttpResponseRedirect('/404/')

	course = []
	ppt_file = []
	ppt_slices = []
	questions =  []
	ppt_slices_data = []
	course_data = []
	question_data = []
	ppt_total_page = 0
	try:
		course  = courses_models.Course.objects.get(id=course_id)
		ppt_file = courses_models.PPTfile.objects.get(course=course,\
		title=ppt_title)
		ppt_slices = courses_models.PPTslice.objects.filter(pptfile=ppt_file,\
		index=slice_index)
		ppt_total_page = len(courses_models.PPTslice.objects.filter(pptfile=ppt_file))
	except:
		return HttpResponseRedirect('/404/')

#	ppt_slices_data = []
	for slice in ppt_slices:
		ps_data = {}
		ps_data['index'] = slice.index
		ps_data['date'] = slice.upload_time
		ps_data['img_path'] = slice.img_path
		ps_data['ppt_total_page'] = ppt_total_page
#		ppt_slices_data.append(ps_data)
		# we only process 1 slice each time at now.
		ppt_slices_data = ps_data

	course_data = {}
	course = courses_models.Course.objects.get(id=course_id)
	course_data['id'] = course.id
	course_data['course_id'] = course.course_id
	course_data['title'] = course.title
#	teachers = course.teacher.all()
#	teacher_data = []
#	for i in range(len(teachers)):
#		teacher_data.append(teachers[i].username)
#	course_data['teacher'] = teacher_data
	course_data['teacher'] = course.teacher_name 

	tas = course.teaching_assitant.all()
	tas_data = []
	for i in range(len(tas)):
		tas_data.append(tas[i].username)
	course_data['teaching_assistant'] = tas_data
	course_data['date'] = course.create_time

	questions = comments_views.get_question(course_id, ppt_title, slice_index)
	question_data = []
	for q in questions:
		q_data = {}

		#get basic info about the certain question
		q_data['question_id'] = q.id
		q_data['username'] = q.user.username
		user_avatar = q.user.useravatar.name
		if user_avatar == '' or user_avatar =='NULL':
			user_avatar = 'avatar/default.png'
		q_data['user_avatar'] = '/media/'+user_avatar
		q_data['date'] = q.date
		q_data['content'] = q.content
		q_data['num_vote'] = q.num_vote

		#add comments on this question
		question_comments = comments_views.get_question_comment(q)
		question_comments_data = []
		for qc in question_comments:
				qc_data = {}
				qc_data['username'] = qc.user.username
				user_avatar = q.user.useravatar.name
				if user_avatar == '' or user_avatar =='NULL':
					user_avatar = 'avatar/default.png'
				qc_data['user_avatar'] = '/media/'+user_avatar
				qc_data['date'] = qc.date
				qc_data['content'] = qc.content
				question_comments_data.append(qc_data)

		q_data['question_comments'] = question_comments_data
		#get answers of this question
		answers = comments_views.get_answer(q)
		answers_data = []
		for a in answers:
			a_data = {}
			a_data['answer_id'] = a.id
			a_data['username'] = a.user.username
			user_avatar = q.user.useravatar.name
			if user_avatar == '' or user_avatar =='NULL':
				user_avatar = 'avatar/default.png'
			a_data['user_avatar'] = '/media/'+user_avatar
			a_data['date'] = a.date
			a_data['content'] = a.content
			a_data['num_vote'] = a.num_vote

			#add comments of this answer
			answer_comments = comments_views.get_answer_comment(a)
			answer_comments_data = []
			for ac in answer_comments:
				ac_data = {}
				ac_data['username'] = ac.user.username
				user_avatar = q.user.useravatar.name
				if user_avatar == '' or user_avatar =='NULL':
					user_avatar = 'avatar/default.png'
				ac_data['user_avatar'] = '/media/'+user_avatar
				ac_data['date'] = ac.date
				ac_data['content'] = ac.content
				answer_comments_data.append(ac_data)

			a_data['answer_comments'] = answer_comments_data
			answers_data.append(a_data)


		q_data['answers'] = answers_data
		question_data.append(q_data)

	user_data = request.user.username
	print('question_data')
	print(question_data)

	print('ppt_slices_data')
	print(ppt_slices_data)

	print('course_data')
	print(course_data)
	print('user_data')
	print(user_data)
	print('ppt_total_page')
	print(ppt_total_page)

	return render_to_response('player.html', {'logined': request.user.is_authenticated(),'user_name':request.user.username,'user_data': user_data, \
	'ppt_slices_data': ppt_slices_data,'course_data':course_data,\
	'question_data':question_data}, context_instance=RequestContext(request))

@login_required
def add_vote(request):
	now = datetime.datetime.now()
	if request.method == 'POST':
		print(request.POST)
		code = -1
		msg = '请检查是否登录'
		new_answer_id = -4
		user_id = int(request.user.id)
		question_id = int(request.POST['question_id'])
		answer_id = int(request.POST['answer_id'])
		course_id = int(request.POST['course_id'])
		ppt_file_title = request.POST['ppt_file_title']
		ppt_slice_id = int(request.POST['ppt_slice_id'])

		curr_user = users_models.User.objects.get(id=user_id)

		#vote on a question
		if answer_id < 0:
			curr_question = comments_models.Question.objects.filter(id=question_id)
			if curr_question == []:
					msg = '当前的问题不存在'
			else:
				if comments_models.Question_Vote.objects.filter(question=curr_question[0], user=curr_user):
					msg = '您已经点过赞了'

				else:
					print('curr_question:')
					print(curr_question)
					print('curr_user:')
					print(curr_user)
					new_qv = comments_models.Question_Vote(date=now, question=curr_question[0], user=curr_user);
					new_qv.save()

					curr_question.update(num_vote=curr_question[0].num_vote+1)
					code = 0
					msg = ''

		#vote on an answer
		else:
			curr_answer= comments_models.Answer.objects.filter(id=answer_id)
			if curr_answer == []:
					msg = '当前的回答不存在'
			else:
				if comments_models.Answer_Vote.objects.filter(answer=curr_answer[0], user=curr_user):
					msg = '您已经点过赞了'
				else:
					print('curr_answer:')
					print(curr_answer)
					print('curr_user:')
					print(curr_user)
					new_av = comments_models.Answer_Vote(date=now, answer=curr_answer[0], user=curr_user);
					new_av.save()
					curr_answer.update(num_vote=curr_answer[0].num_vote+1)
					code = 0
					msg = ''

		return HttpResponse(json.dumps({'code':code, 'msg': msg, 'answer_id':\
		new_answer_id}), content_type="application/json")

	else:
		return HttpResponse(json.dumps({'code':0, 'msg': '0', 'answer_id' : 0}),\
		content_type="application/json")

@login_required
def add_comments(request):
	now = datetime.datetime.now()
	user_avatar = request.user.useravatar.name
	if user_avatar == '' or user_avatar =='NULL':
		user_avatar = 'avatar/default.png'
	user_avatar = '/media/'+user_avatar
	if request.method == 'POST':
		print(request.POST)
		code = -1
		msg = '请检查是否登录'
		new_answer_id = -4
		new_question_id = -4
		content = request.POST['content']
		user_id = int(request.user.id)
		question_id = int(request.POST['question_id'])
		answer_id = int(request.POST['answer_id'])
		course_id = int(request.POST['course_id'])
		ppt_file_title = urllib.unquote(request.POST['ppt_file_title'])
		#change the unicode type variable to str variable 
		ppt_file_title = ppt_file_title.encode('latin-1')
		ppt_slice_id = int(request.POST['ppt_slice_id'])

		curr_user = users_models.User.objects.get(id=user_id)

		#create a question
		if answer_id == -5:
			course = courses_models.Course.objects.get(id=course_id)
			ppt_file = courses_models.PPTfile.objects.get(course=course, \
			title=ppt_file_title)
			ppt_slice = courses_models.PPTslice.objects.get(pptfile=ppt_file, \
			index=ppt_slice_id)

			new_question = comments_models.Question(date=now, user=request.user,\
			course=course,ppt_file=ppt_file, ppt_slice=ppt_slice, content=content,\
			num_vote = 0)
			new_question.save()
			new_question_id = new_question.id
			code = 0
			msg = ''

		#create an answer
		elif answer_id == -2:
			course = courses_models.Course.objects.get(id=course_id)
			question = comments_models.Question.objects.get(id=question_id)
#			curr_user_role = .Answer.objects.get(id=comment_id)
			new_answer= comments_models.Answer(date=now, user=request.user,\
			course=course, question=question, user_role=request.user.user_role,\
			content=content, num_vote=0)
			new_answer.save()
			new_answer_id = new_answer.id
			code = 0
			msg = ''

		#comment on a quesiton
		elif answer_id == -1:
			curr_question = comments_models.Question.objects.get(id=question_id)
			new_qc = comments_models.Question_Comment( \
			date = datetime.datetime.now(),\
			question = curr_question, user = curr_user, content=content)
			new_qc.save()
			code = 0
			msg = ''

		#comment on an answer
		elif answer_id >= 0:
			curr_answer = comments_models.Answer.objects.get(id=answer_id)
			new_ac = comments_models.Answer_Comment( \
			date = datetime.datetime.now(),\
			answer = curr_answer, user = curr_user, content=content)
			new_ac.save()
			code = 0
			msg = ''

		return HttpResponse(json.dumps({'code':code, 'msg': msg,\
		'answer_id':new_answer_id, 'question_id': new_question_id, 'user_avatar': user_avatar}), \
		content_type="application/json")

	else:
		return HttpResponse(json.dumps({'code':0, 'msg': '','user_avatar': user_avatar}), content_type= \
		"application/json")

def page_change(request):
	page_num = 12
	code = '-1'
	msg = '未知错误'
	if request.method == 'POST':
		print('=============post:')
		print(request.POST)
		page_id = int(request.POST['page_id'])
		begin_num = (page_id - 1) * page_num
		end_num = (page_id) * page_num
		all_courses = courses_models.Course.objects.all().order_by('id')
		total_num = all_courses.count()
		if total_num < end_num:
			end_num = total_num
		curr_courses = all_courses[begin_num:end_num]
		item_count = end_num - begin_num
		courses_data = []
		for cc in curr_courses:
			cc_data = {}
			cc_data['id'] = cc.id
			cc_data['title'] = cc.title
			#transfer the datetime object to string and remove its hh:mm:ss
			cc_data['create_time'] = str(cc.create_time).split(' ')[0]
			cc_data['teacher_name'] = cc.teacher_name
			courses_data.append(cc_data)
			code = '0'
			msg = ''
		
		print('course:')
		print(courses_data)
		print('item_count:')
		print(item_count)
		return HttpResponse(json.dumps({'code':code, 'msg': msg,\
		'course':courses_data, 'item_count': item_count}), \
		content_type="application/json")

	else:
		return HttpResponse(json.dumps({'code':0, 'msg': ''}), content_type= \
		"application/json")

	
def feedback(request):
	if request.method == "POST":
		user = request.user
		if user.is_anonymous():
			user = None
		date = datetime.datetime.now()
		content = request.POST['content']
		feedback = digital_models.Feedback(date=date, user=user, content=content)
		feedback.save()
		send_mail(
			'feedback',
			content,
			None,
			['ustcfighters@126.com'],
			fail_silently=False
		)
		return HttpResponseRedirect('/thanks/')
	else:
		return render_to_response('feedback.html', {'logined': request.user.is_authenticated(), 'user_name':request.user.username},context_instance= \
		RequestContext(request))

def thanks(request):
	return render_to_response('thanks.html', {'logined': request.user.is_authenticated(), 'user_name':request.user.username})
def building(request):
	return render_to_response('building.html', {'logined': request.user.is_authenticated(), 'user_name':request.user.username})
# why this does not work?
def create(request):
    if request.user.user_role=="st":
        return render_to_response("premissionDeniey.html")
    return render_to_response('create.html')

# for logout quiet;
# but it seems doesn't work'
@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/?message=logout")#request.META.get('HTTP_REFERER', '/'))

@login_required
def courses(request):
    return HttpResponseRedirect("CourseList/Chapter01.html")

def page_404(request):
	return render_to_response('404.html')

def video(request, course_id, video_title):
	try:
		course_id = int(course_id)
	except ValueError:
		return HttpResponseRedirect('/404/')
	course = []
	video = None
	video_comments = []
	video_comments_data = []
	try:
		print('course')
		course  = courses_models.Course.objects.get(id=course_id)
#		print(course)
		video = courses_models.Video.objects.filter(course=course,\
		title=video_title)[0]
#		print(video)
		video_comments = comments_models.Video_Comment.objects.\
		filter(video=video)
	except:
		return HttpResponseRedirect('/404/')

	course_data = {}
	course_data['id'] = course_id
#	video comments data
	video_data = {}
	video_data['index'] = video.index
	video_data['introduce'] = video.introduce
	video_data['upload_time'] = video.upload_time
	video_data['title'] = video.title
	video_data['path'] = video.video_path

	for vc in video_comments:
		vc_data = {}
		vc_data['date'] = vc.date
		vc_data['user_name'] = vc.user.username
		user_avatar = vc.user.useravatar.name
		if user_avatar == '' or user_avatar =='NULL':
			user_avatar = 'avatar/default.png'
		vc_data['user_avatar'] = '/media/'+user_avatar
		vc_data['content'] = vc.content
		video_comments_data.append(vc_data)

	print('video_data')
	print(video_data)
	print('video_comments_data')
	print(video_comments_data)

	return render_to_response('video_player.html', {'logined': request.user.is_authenticated(),'user_name':request.user.username,'course_data':course_data,'video_data': video_data,'video_comments_data': video_comments_data}, context_instance=RequestContext(request))

	return render_to_response('video_player.html')

@ajax
def add_video_comment(request):
	if  request.method == 'POST':
		now = datetime.datetime.now()
		course_id = int(request.POST['course_id'])
		video_name = request.POST['video_name']
		content = request.POST['content']
		course = courses_models.Course.objects.get(id=course_id)
		video = courses_models.Video.objects.filter(course=course,title=video_name)[0]
		new_vc = comments_models.Video_Comment(date=now,
		video=video,user=request.user,content=content)
		new_vc.save()

		vc_data = {}
		vc_data['date'] = now
		vc_data['user_name'] = request.user.username
		user_avatar = request.user.useravatar.name
		if user_avatar == '' or user_avatar =='NULL':
			user_avatar = 'avatar/default.png'
		user_avatar = '/media/'+user_avatar
		vc_data['content'] = content


		return {'result': 0, 'date':str(now),'user_name': request.user.username,
		'user_avatar': user_avatar, 'content':content}
		#return {'result': 0}

	else:
		return {'result': 0}

def discuss(request):
	content_list = comments_models.Discuss_Comment.objects.filter()
	discuss_data = []
	for content in content_list:
		d_data = {}
		d_data['date'] = content.date
		d_data['user_name'] = content.user
		user_avatar = content.user.useravatar.name
		if user_avatar == '' or user_avatar =='NULL':
			user_avatar = 'avatar/default.png'
		user_avatar = '/media/'+user_avatar
		d_data['user_avatar'] = user_avatar
		d_data['content'] = content.content
		discuss_data.append(d_data)

	return render_to_response('discuss.html', {'logined': request.user.is_authenticated(),'user_name':request.user.username,'discuss_data': discuss_data},context_instance=RequestContext(request))


@ajax
def add_discuss_comment(request):
	if  request.method == 'POST':
		now = datetime.datetime.now()
		content = request.POST['content']
		new_dc = comments_models.Discuss_Comment(date=now,
		user=request.user,content=content)
		new_dc.save()

		user_avatar = request.user.useravatar.name
		if user_avatar == '' or user_avatar =='NULL':
			user_avatar = 'avatar/default.png'
		user_avatar = '/media/'+user_avatar

		return {'result': 0, 'date':str(now),'user_name': request.user.username,
		'user_avatar': user_avatar, 'content':content}

	else:
		return {'result': 0}


		

