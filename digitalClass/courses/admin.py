from django.contrib import admin

# Register your models here.
from courses.models import *

admin.site.register(User2)
admin.site.register(Question)
admin.site.register(Course)
admin.site.register(Answer)

