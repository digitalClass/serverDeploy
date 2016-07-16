#!coding:utf8
from django.http import HttpResponseRedirect,HttpResponse
from django.template import Template,Context,loader, RequestContext
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import datetime

from comments import models as comments_models
from comments import views as comments_views
from users import models as users_models 
from courses import models as courses_models
from courses import views as courses_views

from users.models import User

now = datetime.datetime.now()
def homepage(request):
    if not request.user.is_authenticated():
        return render_to_response("index.html")
    else:
        html = "<html><h1>need to be doen<h1><a href='/accounts/logout/'>注销</a></html>"
        return HttpResponse(html)

@login_required
def profile(request):
    if request.user.is_authenticated():
        user_email = request.user.email
        user_name = request.user.username
        user_id = request.user.id
        # te:Teacher;ta:TeachAssisstant;st:Student
        user_role = request.user.user_role
    return render_to_response('users/profile.html',{"user_name":user_name,})

def classroom(request, course_id, ppt_title, slice_id):
	ppt_file = courses_models.PPTfile.objects.get(course=course_id, title=ppt_title)
	ppt_slices = courses_models.PPTslice.objects.filter(pptfile=ppt_file, index=slice_id)

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
	teacher_data = {}
	for i in range(len(teachers)):
		teacher_data[str(i)] = teachers[i].username
	course_data['teacher'] = teacher_data

	tas = course.teaching_assitant.all()
	tas_data = {}
	for i in range(len(tas)):
		tas_data[str(i)] = tas[i].username
	course_data['teaching_assistant'] = tas_data
	course_data['date'] = course.create_time


	questions = comments_views.get_question(course_id, ppt_title, slice_id)
	question_data = []	
	for q in questions:
		q_data = {}

		#get basic info about the certain question
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

	print('question_data')
	print(question_data)

	print('ppt_slices_data')
	print(ppt_slices_data)

	print('course_data')
	print(course_data)
	return render_to_response('player.html', {'ppt_slices_data': ppt_slices_data,'course_data':course_data,'question_data':question_data}, context_instance=RequestContext(request))

@login_required
def add_comments(request):
	if request.method == 'POST':
		code = -1
		msg = '未知错误'
		content = request.POST['content']
		user_id = request.POST['userid']
		comment_type = request.POST['comment_type']
		comment_id = request.POST['comment_id']
		curr_user = users_models.User.objects.get(id=user_id)
		if comment_type == 0:
			curr_question = comments_models.Questiion.objects.get(id=comment_id)
			new_qc = comments_models.Question_Comment( \
			date = datetime.datetime.today(),\
			question = curr_question, \
			user = curr_user)
			new_qc.save()
			code = 0
			msg = ''

		else:
			curr_answer = comments_models.Answer.objects.get(id=comment_id)
			new_ac = comments_models.Answer_Comment( \
			date = datetime.datetime.today(),\
			answer = curr_answer, \
			user = curr_user)
			new_ac.save()
			code = 0
			msg = ''

		render_to_response('addcomments.html', {'code':code, 'msg': msg}, \
		context_instance= RequestContext(request))
		
	else:
		render_to_response('addcomments.html', {'code':0, 'msg': ''}, \
		context_instance= RequestContext(request))

	
# why this does not work?
def create(request):
    return render_to_response('create.html')

# for logout quiet;
# but it seems doesn't work'
@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
