#TM又不做测试集，这里用python帮我自动做
import os
import shutil
sourcePath="D:/tmp/mycifar10_data/Train"
targetPath="D:/tmp/mycifar10_data/Evel"
def moveFile(sourceFile,targetFile,p=0.2):		#p即测试集的占比
	photo_list=os.listdir(sourceFile)
	sum=len(photo_list)
	move_num=int(sum*p)
	i=0
	for photo in photo_list:
		if not i<move_num:
			break
		photo_sourcePath=os.path.join(sourceFile,photo)
		shutil.move(photo_sourcePath,targetFile)
		i+=1
	
for file in os.listdir(sourcePath):
	sourceFile=os.path.join(sourcePath,file)
	targetFile=os.path.join(targetPath,file)
	os.mkdir(targetFile)
	moveFile(sourceFile,targetFile)
	
