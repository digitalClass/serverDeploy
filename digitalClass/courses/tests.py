from django.test import TestCase
from users import models as users_models
from courses.models import Course
import datetime
from django.utils import timezone 

print "import OK"
now = timezone.now()
print now
#zhang = users_models.User.objects.create(username='zhang', student_id='SA15006070', email='zhang@mail.ustc.edu.cn', password='123456', user_role='st',gender='m')
#cobby = users_models.User.objects.create(username='cobby', student_id='PB11210098', email='cobby@mail.ustc.edu.cn', password='123456', user_role='te',gender='m')
class CreateTestCase(TestCase):
    def setUp(self):
	Course.objects.create(introduce='This is a math course', create_time=now, img_path='/courses/1.jpg', title='math', course_id='MATH_A')
	Course.objects.create(introduce='This is a English course', create_time=now, img_path='/courses/1.jpg', title='English', course_id='ENGLISH_A')
	print "CreateTestCase_setUp is right"
    def test_Course(self):
	math = Course.objects.get(title='math')
	english = Course.objects.get(title='english')
	print math.title,math.introduce,math.create_time,math.img_path,math.course_id
	print english






