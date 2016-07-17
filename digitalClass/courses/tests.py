from django.test import TestCase
from courses.models import Course
import datetime
from django.utils import timezone 

print "import OK"
now = timezone.now()
print now
# Create your tests here.
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






