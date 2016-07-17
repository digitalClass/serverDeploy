from django.test import TestCase
from courses import models
from users import models as users_models
import datetime
# Create your tests here.
cobby = users_models.User.objects.create(username='cobby', student_id='PB11210098', email='ycz0098@mail.ustc.edu.cn', password='123456', user_role='te',gender='m')
zhang = users_models.User.objects.create(username='zhang', student_id='SA15006070', email='ycz0098@mail.ustc.edu.cn', password='123456', user_role='st',gender='m')
class CourseTestCase(TestCase):
    def setUp(self):
	now = datetime.datetime.now()
	Course.objects.create(introduce='This is a math class', create_time=now, img_path='courses/test_img.jpg)', title='math', course_id='ABC123' )
	math.teacher.add(cobby)
    def testCourseCreate(self):
	math = Course.objects.get(title='math')	
	math.tercher.all()
	cobby.teacher.all()










