#!coding:utf8
from django.http import HttpResponseRedirect,HttpResponse
from django.template import Template,Context,loader, RequestContext
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import datetime
import json

from comments import models as comments_models
from comments import views as comments_views
from users import models as users_models
from courses import models as courses_models
from courses import views as courses_views
from digitalClass import models as digital_models
from django.core.mail import send_mail

from users.models import User

now = datetime.datetime.now()
def homepage(request):
    # 不用登陆也能看到课程列表
    courses = courses_models.Course.objects.all()
    if request.user.is_authenticated():
        username = request.user.username
        user_id = request.user.id
        # te:Teacher;ta:TeachAssisstant;st:Student
        user_role = request.user.user_role
        return render_to_response("index.html",{"logined":True,'user_name':username,'user_id':user_id,'user_role':user_role,"courses":courses})
    else:
        return render_to_response("index.html",{"logined": False,"courses":courses})

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
	course  = courses_models.Course.objects.get(id=course_id)
	ppt_file = courses_models.PPTfile.objects.get(course=course, title=ppt_title)
	ppt_slices = courses_models.PPTslice.objects.filter(pptfile=ppt_file, index=slice_index)

#	ppt_slices_data = []
	for slice in ppt_slices:
		ps_data = {}
		ps_data['index'] = slice.index
		ps_data['date'] = slice.upload_time
		ps_data['img_path'] = slice.img_path
#		ppt_slices_data.append(ps_data)
		# we only process 1 slice each time at now.
		ppt_slices_data = ps_data

	course_data = {}
	course = courses_models.Course.objects.get(id=course_id)
	course_data['course_id'] = course.course_id
	course_data['title'] = course.title
	teachers = course.teacher.all()
	teacher_data = []
	for i in range(len(teachers)):
		teacher_data.append(teachers[i].username)
	course_data['teacher'] = teacher_data

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
		q_data['date'] = q.date
		q_data['content'] = q.content
		q_data['num_vote'] = q.num_vote

		#add comments on this question
		question_comments = comments_views.get_question_comment(q)
		question_comments_data = []
		for qc in question_comments:
				qc_data = {}
				qc_data['username'] = qc.user.username
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
			a_data['date'] = a.date
			a_data['content'] = a.content
			a_data['num_vote'] = a.num_vote

			#add comments of this answer
			answer_comments = comments_views.get_answer_comment(a)
			answer_comments_data = []
			for ac in answer_comments:
				ac_data = {}
				ac_data['username'] = ac.user.username
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

	return render_to_response('player.html', {'user_data': user_data, 'ppt_slices_data': ppt_slices_data,'course_data':course_data,'question_data':question_data}, context_instance=RequestContext(request))

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
				curr_question.update(num_vote=curr_question[0].num_vote+1)
				code = 0
				msg = ''

		#vote on an answer
		else:
			curr_answer= comments_models.Answer.objects.filter(id=answer_id)
			if curr_answer == []:
					msg = '当前的回答不存在'
			else:
				curr_answer.update(num_vote=curr_answer[0].num_vote+1)
				code = 0
				msg = ''

		return HttpResponse(json.dumps({'code':code, 'msg': msg, 'answer_id':new_answer_id}), content_type="application/json")

	else:
		return HttpResponse(json.dumps({'code':0, 'msg': '0', 'answer_id' : 0}), content_type="application/json")

@login_required
def add_comments(request):
	now = datetime.datetime.now()
	if request.method == 'POST':
		print(request.POST)
		code = -1
		msg = '请检查是否登录'
		new_answer_id = -4
		content = request.POST['content']
		user_id = int(request.user.id)
		question_id = int(request.POST['question_id'])
		answer_id = int(request.POST['answer_id'])
		course_id = int(request.POST['course_id'])
		ppt_file_title = request.POST['ppt_file_title']
		ppt_slice_id = int(request.POST['ppt_slice_id'])

		curr_user = users_models.User.objects.get(id=user_id)

		#create a question
		if answer_id == -5:
			course = courses_models.Course.objects.get(id=course_id)
			ppt_file = courses_models.PPTfile.objects.get(course=course, \
			title=ppt_file_title)
			ppt_slice = courses_models.PPTslice.objects.get(pptfile=ppt_file, index=ppt_slice_id)

			new_question = comments_models.Question(date=now, user=request.user,\
			course=course,ppt_file=ppt_file, ppt_slice=ppt_slice, content=content,\
			num_vote = 0)
			new_question.save()
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

		return HttpResponse(json.dumps({'code':code, 'msg': msg, 'answer_id':new_answer_id}), content_type="application/json")

	else:
		return HttpResponse(json.dumps({'code':0, 'msg': ''}), content_type="application/json")

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
		return render_to_response('feedback.html', context_instance=RequestContext(request))

def thanks(request):
	return render_to_response('thanks.html')

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
