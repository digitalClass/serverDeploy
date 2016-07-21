from PIL import Image
import os
import subprocess

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


def split_pdf(pdf_path,save_dir=None):
	file, ext = os.path.splitext(pdf_path)
	if save_dir == None:
		save_dir = os.path.split(pdf_path)[0]
	try:
		subprocess.call(['convert', pdf_path, save_dir+'/%d.jpg'])
	except:
		pass


if __name__ == '__main__':
	create_thumbnail('/media/digitalClass/ppts/2/1.jpg')
	split_pdf('/home/yunfeng/splitpdf/cv.pdf')


