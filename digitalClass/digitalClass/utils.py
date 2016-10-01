#coding:utf-8
from PIL import Image
import os
import subprocess
import glob
from courses.models import PPTslice,PPTfile,Course
from django.http import HttpResponseRedirect,Http404,HttpResponse
from celery.task import task

'''
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
'''

@task
def split_pdf(pdf_path,course_id,ppt_title,save_dir=None):
    '''
    pdf切分函数  出错将直接终止切分，则该课程将不会有切分后的课件 
    
    Args:
        pdf_path  pdf的绝对路径
        course_id  对应课程的课程编号
        ppt_title  课件名称
        save_dir=None  可选的储存位置

   
    '''
    file, ext = os.path.splitext(pdf_path)
    #print file.split('/')[-3]
    if save_dir == None:
        save_dir = os.path.split(pdf_path)[0]
    try:
        # split pdf file
        subprocess.call(['convert', '-verbose',  pdf_path, '-quality', '100', save_dir+'/%d.jpg'])
        # get all the ppt file of this course
        course = Course.objects.get(id=course_id)
        pptfile = course.pptfile_set.filter(title=ppt_title)
        # create PPTslice after spliting pdf file
        for pptslice in glob.glob(os.path.join(save_dir,"*.jpg")):
	    name = os.path.split(pptslice)[1].split('.')[0]
	    index = int(name)+1 # index must > 0
	    PPTslice.objects.create(index=index, img_path=pptslice, pptfile=pptfile[0])
        '''
        之前具有创建课程缩略图的功能，后来被手动上传和使用默认图像代替
        if create_img:
            pardir = os.path.join(save_dir, os.pardir)
            create_thumbnail(os.path.join(save_dir,'0.jpg'),save_dir=pardir)
            img_path = glob.glob(os.path.join(pardir,'*.thumbnail'))[0]
            parent_dir = os.path.dirname(os.path.dirname(pardir))
            parent_url_dir = parent_dir[0:6]+parent_dir[19:]
            img_ur_path = parent_url_dir+'/0.thumbnail'
            course.img = img_ur_path
            course.save()
        '''
    except:
	pass
	#raise Http404()




if __name__ == '__main__':
	create_thumbnail('/media/digitalClass/ppts/2/1.jpg')
	split_pdf('/home/yunfeng/splitpdf/cv.pdf')


