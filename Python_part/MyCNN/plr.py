import tensorflow as tf
import sys
import os
import numpy as np

from . import mycifar10

FLAGS=tf.app.flags.FLAGS
tf.app.flags.DEFINE_string('checkpoint_dir', 'D:/tmp/mycifar10_train',
						"""Directory where to read model checkpoints.""")

global mygraph,mysession,images_batch,character,logits,predictions,label_list,keep_prob			
def init_tensorflow():
	global mygraph,mysession,images_batch,character,logits,predictions,label_list,keep_prob
	label_list=mycifar10.setBATCH_SIZE_and_NUM_CLASSES_and_get_label_list()
	mygraph=tf.Graph()
	with mygraph.as_default():
		images_batch=tf.placeholder(tf.float32,shape=[1,FLAGS.photo_resize,FLAGS.photo_resize,3])
		keep_prob=tf.placeholder(tf.float32)
		character,logits=mycifar10.inference(images_batch,keep_prob)
		predictions=tf.argmax(logits,1)             #tf.argmax取最大值，1 则 第一维度
		# variable_averages = tf.train.ExponentialMovingAverage(mycifar10.MOVING_AVERAGE_DECAY)
		# variables_to_restore = variable_averages.variables_to_restore()
		saver = tf.train.Saver(tf.global_variables())
		mysession=tf.Session()
		ckpt = tf.train.get_checkpoint_state(FLAGS.checkpoint_dir)
		if ckpt and ckpt.model_checkpoint_path:
			saver.restore(mysession, ckpt.model_checkpoint_path)
			#global_step = ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1]
		else:
			raise Exception('No checkpoint file found')

def plr(photo_path_list):
	global mygraph,mysession,images_batch,character,logits,predictions,label_list,keep_prob
	images=mycifar10.cope_judgeimage(photo_path_list)
	with mygraph.as_default():
		character_result,_,predictions_result=mysession.run([character,logits,predictions],feed_dict={images_batch:images,keep_prob:1})
	# for i in range(len(photo_path_list)):
				# print(i,label_list[predictions_result[i]],photo_path_list[i])
	return character_result.tolist(),predictions_result							#将numpy.ndarrary转化为list
	
def input_photo(photo_path):
	global label_list
	photo_path_list=[photo_path]
	for image_path in photo_path_list:
		if not os.path.exists(image_path):
			raise Exception('Please supply a exist image path:',image_path)
	character_result,predictions_result=plr(photo_path_list)
	clear_character_result=[round(x,4) for x in character_result[0]]		#仅保留4位小数（原先十多位）
	# print("character:",clear_character_result)
	return clear_character_result,label_list[predictions_result[0]]

if __name__=='__main__':
	init_tensorflow()
	photo_path="D:/tmp/mycifar10_data/Train/car/full/1.jpg"
	input_photo(photo_path=photo_path)