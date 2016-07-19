from django import forms

class CreateCourseForm(forms.Form):
    course_title = forms.CharField(max_length=32)
    course_id = forms.CharField(max_length=16)
    course_data = forms.CharField(widget=forms.Textarea)

class UploadPPTForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()	





