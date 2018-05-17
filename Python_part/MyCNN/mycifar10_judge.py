import tensorflow as tf
import sys
import os
import numpy as np

import mycifar10

FLAGS=tf.app.flags.FLAGS
tf.app.flags.DEFINE_string('checkpoint_dir', 'D:/tmp/mycifar10_train',
						"""Directory where to read model checkpoints.""")
def judge(image_path_list):
	images,label_list=mycifar10.cope_judgeimage(image_path_list)
	with tf.Graph().as_default():
		images_batch=tf.placeholder(tf.float32,shape=[len(image_path_list),FLAGS.photo_resize, FLAGS.photo_resize, 3])
		logits=mycifar10.inference(images_batch)
		predictions=tf.argmax(logits,1)             #tf.argmax取最大值，1 则 第一维度
		variable_averages = tf.train.ExponentialMovingAverage(mycifar10.MOVING_AVERAGE_DECAY)
		variables_to_restore = variable_averages.variables_to_restore()
		saver = tf.train.Saver(variables_to_restore)
		with tf.Session() as sess:
			ckpt = tf.train.get_checkpoint_state(FLAGS.checkpoint_dir)
			if ckpt and ckpt.model_checkpoint_path:
				saver.restore(sess, ckpt.model_checkpoint_path)
				global_step = ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1]
			else:
				print('No checkpoint file found')
				return
			logits,predictions=sess.run([logits,predictions],feed_dict={images_batch:images})
            # print(logits)
            # print(predictions)
			for i in range(len(image_path_list)):
				print(i,label_list[predictions[i]],image_path_list[i])

def myjudge_main(argv=None):
    # photo_path_list=sys.argv[1:]
    #photo_path_list=['D:/tmp/mycifar10_data/Train/nv_shangzhuang_chenshan/full/305482610.jpg','D:/tmp/mycifar10_data/Train/nv_shangzhuang_fengyi/full/305472406.jpg']
	photo_path_list=['D:/tmp/mycifar10_data/Train/car/full/1.jpg']
	for image_path in photo_path_list:
		if not os.path.exists(image_path):
			raise Exception('Please supply a exist image path:',image_path)
	judge(photo_path_list)
if __name__=='__main__':
	tf.app.run(main=myjudge_main)