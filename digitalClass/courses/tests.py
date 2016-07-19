from django.test import TestCase
from users import models as users_models
from courses.models import *
import datetime
from django.utils import timezone 

print "import OK"
now = timezone.now()
print now
#zhang = users_models.User.objects.create(username='zhang', student_id='SA15006070', email='zhang@mail.ustc.edu.cn', password='123456', user_role='st',gender='m')
class ModelTest(TestCase):
    def setUp(self):
	cobby = users_models.User.objects.create(username='cobby', student_id='PB11210098', email='cobby@mail.ustc.edu.cn', password='123456', user_role='te',gender='m', is_superuser=0, is_staff=0, is_active=1,date_joined=now)
	Course.objects.create(introduce='This is a math course', create_time=now, img_path='/courses/1.jpg', title='math', course_id='MATH_A')
	Course.objects.create(introduce='This is a English course', create_time=now, img_path='/courses/1.jpg', title='English', course_id='ENGLISH_A')
	print "create_course is right,and the user name is",cobby
	math = Course.objects.get(title='math')
	PPTfile.objects.create(introduce='This is a math course ppt', upload_time=now, title='math_chapter_1', course=math)
	print "create_pptfile is right"
    def test_Course(self):
	print Course.objects.all()
	try:
	    math = Course.objects.get(title='math')
	except Course.DoesNotExist:
	    print "math does not exist"
	else:
	    english = Course.objects.get(title='english')
	    cobby = users_models.User.objects.get(username='cobby')
	    math.teacher.add(cobby)
	    print math.title,math.introduce,math.create_time,math.img_path,math.course_id
	    print '\n',math.teacher.all(),cobby.teacher.all()
    def test_ppt(self):  
	math = Course.objects.get(title='math')
	ppt = PPTfile.objects.get(title='math_chapter_1')
	print ppt.course
	print math.pptfile_set.all()

class ViewsTest(TestCase):
    def setUp(self):
	cobby = users_models.User.objects.create(username='cobby', student_id='PB11210098', email='cobby@mail.ustc.edu.cn', password='123456', user_role='te',gender='m', is_superuser=0, is_staff=0, is_active=1,date_joined=now)
	u = self.client.login(email='cobby@mail.ustc.edu.cn',password='123456')
	print 'login',u
    def test_login(self):
	self.client.post()
