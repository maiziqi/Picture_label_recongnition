import tensorflow as tf
import sys
import os
import numpy as np

from . import mycifar10

FLAGS=tf.app.flags.FLAGS
tf.app.flags.DEFINE_string('checkpoint_dir', 'D:/tmp/mycifar10_train',
						"""Directory where to read model checkpoints.""")

global mygraph,mysession,images_batch,logits,predictions,label_list			
def init_tensorflow():
	global mygraph,mysession,images_batch,logits,predictions,label_list
	label_list=mycifar10.setBATCH_SIZE_and_NUM_CLASSES_and_get_label_list()
	mygraph=tf.Graph()
	with mygraph.as_default():
		images_batch=tf.placeholder(tf.float32,shape=[1,FLAGS.photo_resize,FLAGS.photo_resize,3])
		logits=mycifar10.inference(images_batch)
		predictions=tf.argmax(logits,1)             #tf.argmax取最大值，1 则 第一维度
		variable_averages = tf.train.ExponentialMovingAverage(mycifar10.MOVING_AVERAGE_DECAY)
		variables_to_restore = variable_averages.variables_to_restore()
		saver = tf.train.Saver(variables_to_restore)
		mysession=tf.Session()
		ckpt = tf.train.get_checkpoint_state(FLAGS.checkpoint_dir)
		if ckpt and ckpt.model_checkpoint_path:
			saver.restore(mysession, ckpt.model_checkpoint_path)
			#global_step = ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1]
		else:
			raise Exception('No checkpoint file found')

def plr(photo_path_list):
	global mygraph,mysession,images_batch,logits,predictions,label_list
	images=mycifar10.cope_judgeimage(photo_path_list)
	with mygraph.as_default():
		_,predictions_result=mysession.run([logits,predictions],feed_dict={images_batch:images})
	for i in range(len(photo_path_list)):
				print(i,label_list[predictions_result[i]],photo_path_list[i])
	return predictions_result
	
def input_photo(photo_path):
	global label_list
	photo_path_list=[photo_path]
	for image_path in photo_path_list:
		if not os.path.exists(image_path):
			raise Exception('Please supply a exist image path:',image_path)
	predictions=plr(photo_path_list)
	return label_list[predictions[0]]

if __name__=='__main__':
	init_tensorflow()
	photo_path="D:/tmp/mycifar10_data/Train/car/full/1.jpg"
	input_photo(photo_path=photo_path)