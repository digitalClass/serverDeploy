from django.shortcuts import render

from comments.models import Question, Answer, Question_Comment, Answer_Comment
from courses.models import Course, PPTfile, PPTslice
# Create your views here.
def get_question(course_id, ppt_title, slice_index):
	questions = []
	try:
		curr_course = Course.objects.get(id=course_id)	
		curr_ppt_file = PPTfile.objects.get(course=curr_course,title=ppt_title)	

		curr_slice = PPTslice.objects.get(pptfile=curr_ppt_file,index=slice_index)	
		questions = Question.objects.filter(course=curr_course, ppt_file=curr_ppt_file,ppt_slice=curr_slice)
	except:
		pass
	return questions


def get_answer(q):
	answers = []
	try:
		answers= Answer.objects.filter(question=q)	
	except Answer.DoesNotExist:
		pass
	return answers 


def get_question_comment(q):
	question_comments = []
	try:
		question_comments = Question_Comment.objects.filter(question=q)	
	except Question_Comment.DoesNotExist:
		pass
	return question_comments


def get_answer_comment(a):
	answer_comments = []
	try:
		answer_comments = Answer_Comment.objects.filter(answer=a)	
	except Answer_Comment.DoesNotExist:
		pass
	return answer_comments
