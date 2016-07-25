from PIL import Image
import os
import subprocess
import glob
from courses.models import PPTslice,PPTfile,Course
import datetime
from django.http import HttpResponseRedirect,Http404,HttpResponse


def create_thumbnail(img_path,save_dir=None,size=(128,128)):
	file, ext = os.path.splitext(img_path)
	print(file)
	print(save_dir)
	im = Image.open(img_path)
	im.thumbnail(size)
	#default save path is the original image's path
	if save_dir == None:
		im.save(file + '.thumbnail', 'JPEG')
	else:
		file_name = file.split('/')[-1]
		print(file_name)
		im.save(os.path.join(save_dir,file_name) +'.thumbnail', 'JPEG')


def split_pdf(pdf_path,course_id,ppt_title,save_dir=None):
	file, ext = os.path.splitext(pdf_path)
	print file
	if save_dir == None:
		save_dir = os.path.split(pdf_path)[0]
	try:
		subprocess.call(['convert', pdf_path, save_dir+'/%d.jpg'])
		now = datetime.datetime.now()
		for pptslice in glob.glob(os.path.join(save_dir,"*.jpg")):
			
			name = os.path.split(pptslice)[1].split('.')[0]
			index = int(name)+1
			course = Course.objects.get(id=course_id)
			pptfile = course.pptfile_set.filter(title=ppt_title)
			if pptfile:
				ppt = PPTslice.objects.create(index=index, upload_time=now, img_path=pptslice, pptfile=pptfile[0])
	except:
		pass
		#raise Http404()




if __name__ == '__main__':
	create_thumbnail('/media/digitalClass/ppts/2/1.jpg')
	split_pdf('/home/yunfeng/splitpdf/cv.pdf')


