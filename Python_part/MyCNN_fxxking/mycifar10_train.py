import tensorflow as tf
from tensorflow.python.platform import gfile  
from datetime import datetime  
import os
import time 
import numpy as np
import math####
import mycifar10

FLAGS=tf.app.flags.FLAGS

tf.app.flags.DEFINE_integer('step_num',5000,
							"""the number of run step .""")
tf.app.flags.DEFINE_string('train_dir', 'D:/tmp/mycifar10_train',  					
							"""Directory where to write event logs and checkpoint.""")
tf.app.flags.DEFINE_integer('batch_size',120,
							"""Number of images to process in a batch.""")
tf.app.flags.DEFINE_integer('restore_bool',1,
							"""restore the checkpoint.""")
def train():
	#print(FLAGS.restore_bool)
	dict,label_list=mycifar10.prepare_datadict('Train')
	Evel_dict,Evel_label_list=mycifar10.prepare_datadict('Evel')
	with tf.Graph().as_default():
		global_step = tf.Variable(0, trainable=False,name='global_step')
		#img_batch,label_batch=mycifar10.train_distorted_inputs()
		# img_batch, label_batch = mycifar10.train_distorted_inputs(dict)
		image_batch=tf.placeholder(tf.float32,shape=[FLAGS.batch_size,FLAGS.photo_resize,FLAGS.photo_resize,3])
		label_batch=tf.placeholder(tf.int32,shape=[FLAGS.batch_size])
		keep_prob=tf.placeholder(tf.float32)
		logits=mycifar10.inference(image_batch,keep_prob)
		top_k_op=tf.nn.in_top_k(logits,label_batch,1)####
		loss=mycifar10.loss(logits,label_batch)
		train_op=mycifar10.train(loss,global_step)

		saver=tf.train.Saver(tf.global_variables())

		init=tf.initialize_all_variables()

		print("Start")
		with tf.Session() as sess:
			restore_global_step=0
			if not FLAGS.restore_bool:		#如果是第一次训练，就初始化所有变量
				sess.run(init)
			else:
				ckpt = tf.train.get_checkpoint_state(FLAGS.train_dir)  	
				#print(ckpt.model_checkpoint_path)
				if ckpt and ckpt.model_checkpoint_path:  
					saver.restore(sess, ckpt.model_checkpoint_path)
					restore_global_step = int(ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1])  
					#print(restore_global_step)
				else:  
					print('No checkpoint file found')  
					return  
			#tf.train.start_queue_runners(sess=sess)
			for step in range(FLAGS.step_num):
				# print(step+restore_global_step)
				images, labels = mycifar10.distorted_inputs(dict,label_list,'Train')
				#print(labels)	
				start_time=time.time()
				_,loss_value=sess.run([train_op,loss],feed_dict={image_batch:images,label_batch:labels,keep_prob:0.5})
				duration=time.time()-start_time
				assert not np.isnan(loss_value), 'Model diverged with loss = NaN'
				if step%10==0:
					examples_per_sec=FLAGS.batch_size/duration
					sec_per_batch=float(duration)
					format_str=('%s: step %d, loss = %.2f (%.1f examples/sec; %.3f '  	#%.2f表示 保留小数点后2位的float 的占位符
							  'sec/batch)')
					print(format_str % (datetime.now(), step+restore_global_step, loss_value,
									examples_per_sec, sec_per_batch))
				if step%100==0 or (step+1)==FLAGS.step_num:
					checkpoint_path = os.path.join(FLAGS.train_dir, 'model.ckpt')
					saver.save(sess, checkpoint_path, global_step=step+restore_global_step)
				if step%50==0:
					test_num=int(math.ceil(300/FLAGS.batch_size))
					actually_total_example=test_num*FLAGS.batch_size
					true_count=0
					s=0
					while s<test_num:
						images, labels = mycifar10.distorted_inputs(dict,label_list,'Train')
						predictions=sess.run([top_k_op],feed_dict={image_batch:images,label_batch:labels,keep_prob:1.0})
						true_count+=np.sum(predictions)
						s+=1
					precision=true_count/actually_total_example
					print('%s: Train precision @ 1 = %.3f' % (datetime.now(), precision))
					
					test_num=int(math.ceil(300/FLAGS.batch_size))
					actually_total_example=test_num*FLAGS.batch_size
					true_count=0
					s=0
					while s<test_num:
						images, labels = mycifar10.distorted_inputs(Evel_dict,Evel_label_list,'Evel')
						predictions=sess.run([top_k_op],feed_dict={image_batch:images,label_batch:labels,keep_prob:1.0})
						true_count+=np.sum(predictions)
						s+=1
					precision=true_count/actually_total_example
					print('%s: Evel precision @ 1 = %.3f' % (datetime.now(), precision))
		print("Finish")

def mytrain_main(argv=None):
	if not FLAGS.restore_bool:
		if gfile.Exists(FLAGS.train_dir):
			gfile.DeleteRecursively(FLAGS.train_dir)
		gfile.MakeDirs(FLAGS.train_dir)
	train()
	
if __name__=='__main__':
	tf.app.run(main=mytrain_main)