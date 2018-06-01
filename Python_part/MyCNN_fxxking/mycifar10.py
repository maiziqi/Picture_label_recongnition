import tensorflow as tf
import os
import random
import numpy
import math
from PIL import Image

#import mycifar10_input
FLAGS=tf.app.flags.FLAGS
tf.app.flags.DEFINE_string('image_data_path','D:/tmp/mycifar10_data',
						   """The path of image""")
tf.app.flags.DEFINE_integer('photo_resize',227,						##s:32
							"""resize the photo""")
# tf.app.flags.DEFINE_string('TFdata_dir','D:/tmp/mycifar10_data/TFRecords',
# 							"""Path to the photo(TFRecords) data directory.""")
# tf.app.flags.DEFINE_integer('save_photo_size',224,
# 							"""TFRecords save photo size.""")				#生成TFRecords文件时，按照这个尺寸存放图片

global NUM_CLASSES,BATCH_SIZE
NUM_EXAMPLES_PER_EPOCH_FOR_TRAIN=300

NUM_EPOCHS_PER_DECAY=350.0
LEARNING_RATE_DECAY_FACTOR=0.85									#学习递减率
INITIAL_LEARNING_RATE=0.001									#初始学习率
MOVING_AVERAGE_DECAY=0.9999
							
def _variable_on_cpu(name,shape,initializer):
	with tf.device('/cpu:0'):
		var =tf.get_variable(name,shape,initializer=initializer)
	return var

def _variable_with_weight_decay(name, shape,stddev,wd):
	var = _variable_on_cpu(name,shape,
						tf.truncated_normal_initializer(stddev=stddev))
	# if wd:
		# weight_decay=tf.multiply(tf.nn.l2_loss(var),wd,name='weight_loss')
		# tf.add_to_collection('losses',weight_decay)
	return var

def inference(images,keep_prob):									#keep_prob是有效概率
	# myconv1
	with tf.variable_scope('myconv1') as scope:
		kernel=_variable_with_weight_decay('weights',shape=[11,11,3,48],
										stddev=1e-1,wd=0.0)
		conv=tf.nn.conv2d(images,kernel,[1,4,4,1],padding='VALID')
		biases=_variable_on_cpu('biaes',[48],tf.constant_initializer(0.0))
		bias=tf.nn.bias_add(conv,biases)
		myconv1=tf.nn.relu(bias,name=scope.name)
	# mypool1
	mypool1=tf.nn.max_pool(myconv1,ksize=[1,3,3,1],strides=[1,2,2,1],
					padding='VALID',name='mypool1')
	# mynorm1
	mynorm1=tf.nn.lrn(mypool1,4,bias=1.0,alpha=0.001/9.0,beta=0.75,name='mynorm1')
	
	# myconv2
	with tf.variable_scope('myconv2') as scope:
		kernel=_variable_with_weight_decay('weights',shape=[5,5,48,64],
										stddev=1e-1,wd=0.0)
		conv=tf.nn.conv2d(mynorm1,kernel,[1,1,1,1],padding='SAME')
		biases=_variable_on_cpu('biaes',[64],tf.constant_initializer(0.0))
		bias=tf.nn.bias_add(conv,biases)
		myconv2=tf.nn.relu(bias,name=scope.name)
	# mypool2
	mypool2=tf.nn.max_pool(myconv2,ksize=[1,3,3,1],strides=[1,2,2,1],
					padding='VALID',name='mypool2')
	# mynorm2
	mynorm2=tf.nn.lrn(mypool2,4,bias=1.0,alpha=0.001/9.0,beta=0.75,name='mynorm2')
	
	# myconv3
	with tf.variable_scope('myconv3') as scope:
		kernel=_variable_with_weight_decay('weights',shape=[3,3,64,96],
										stddev=1e-1,wd=0.0)
		conv=tf.nn.conv2d(mynorm2,kernel,[1,1,1,1],padding='SAME')
		biases=_variable_on_cpu('biaes',[96],tf.constant_initializer(0.0))
		bias=tf.nn.bias_add(conv,biases)
		myconv3=tf.nn.relu(bias,name=scope.name)
#	# mypool3
#	mypool3=tf.nn.max_pool(myconv3,ksize=[1,3,3,1],strides=[1,2,2,1],
#					padding='VALID',name='mypool3')
#	# mynorm3
#	mynorm3=tf.nn.lrn(mypool3,4,bias=1.0,alpha=0.001/9.0,beta=0.75,name='mynorm3')
	
	# myconv4
	with tf.variable_scope('myconv4') as scope:
		kernel=_variable_with_weight_decay('weights',shape=[3,3,96,96],
										stddev=1e-1,wd=0.0)
		conv=tf.nn.conv2d(myconv3,kernel,[1,1,1,1],padding='SAME')
		biases=_variable_on_cpu('biaes',[96],tf.constant_initializer(0.0))
		bias=tf.nn.bias_add(conv,biases)
		myconv4=tf.nn.relu(bias,name=scope.name)
#	# mypool4
#	mypool4=tf.nn.max_pool(myconv4,ksize=[1,3,3,1],strides=[1,2,2,1],
#					padding='VALID',name='mypool4')
#	# mynorm4
#	mynorm4=tf.nn.lrn(mypool4,4,bias=1.0,alpha=0.001/9.0,beta=0.75,name='mynorm4')
	
	# myconv5
	with tf.variable_scope('myconv5') as scope:
		kernel=_variable_with_weight_decay('weights',shape=[3,3,96,64],
										stddev=1e-1,wd=0.0)
		conv=tf.nn.conv2d(myconv4,kernel,[1,1,1,1],padding='SAME')
		biases=_variable_on_cpu('biaes',[64],tf.constant_initializer(0.0))
		bias=tf.nn.bias_add(conv,biases)
		myconv5=tf.nn.relu(bias,name=scope.name)
	# mypool5
	mypool5=tf.nn.max_pool(myconv5,ksize=[1,3,3,1],strides=[1,2,2,1],
					padding='VALID',name='mypool5')
	# mynorm5
	mynorm5=tf.nn.lrn(mypool5,4,bias=1.0,alpha=0.001/9.0,beta=0.75,name='mynorm5')
	
	# local1
	with tf.variable_scope('local1') as scope:
		dim=1
		for d in mynorm5.get_shape()[1:].as_list():
			dim*=d
		reshape=tf.reshape(mynorm5,[BATCH_SIZE,dim])
		weights=_variable_with_weight_decay('weights',shape=[dim,512],					#384
										stddev=1e-1,wd=0.004)
		biases=_variable_on_cpu('biases',[512],tf.constant_initializer(0.1))
		local1=tf.nn.relu(tf.matmul(reshape,weights)+biases,name=scope.name)
		local1_drop=tf.nn.dropout(local1,keep_prob)			#drop
		
	# local2	
	with tf.variable_scope('local2') as scope:  
		weights = _variable_with_weight_decay('weights', shape=[512, 512],  
											stddev=1e-1, wd=0.004)  
		biases = _variable_on_cpu('biases', [512], tf.constant_initializer(0.1))  
		local2 = tf.nn.relu(tf.matmul(local1_drop, weights) + biases, name=scope.name)  
		local2_drop=tf.nn.dropout(local2,keep_prob)
		
	with tf.variable_scope('softmax_linear') as scope:  
		weights = _variable_with_weight_decay('weights', [512, NUM_CLASSES],  
											  stddev=1e-1, wd=0.0)  
		biases = _variable_on_cpu('biases', [NUM_CLASSES],  
								  tf.constant_initializer(0.1))  
		softmax_linear = tf.add(tf.matmul(local2_drop, weights), biases, name=scope.name)  
		
		
	return softmax_linear

###################################################################

def loss(logits,labels):
	indices=tf.reshape(tf.range(BATCH_SIZE),[BATCH_SIZE,1])
	sparse_labels=tf.reshape(labels,[BATCH_SIZE,1])
	concated=tf.concat([indices,sparse_labels],1)
	dense_labels=tf.sparse_to_dense(concated,
									[BATCH_SIZE,NUM_CLASSES],
									1.0,0.0)
	cross_entropy=tf.nn.softmax_cross_entropy_with_logits(logits=logits,labels=dense_labels,name='cross_entropy_per_example')
	cross_entropy_mean=tf.reduce_mean(cross_entropy,name='cross_entropy')
	# tf.add_to_collection('losses',cross_entropy_mean)
	
	#return tf.add_n(tf.get_collection('losses'),name='total_loss')
	return cross_entropy_mean
	
###################################################################

def _add_loss_summaries(total_loss):
	loss_averages=tf.train.ExponentialMovingAverage(0.9,name='avg')
	losses=tf.get_collection('losses')
	loss_averages_op=loss_averages.apply(losses+[total_loss])
	
	return loss_averages_op

def train(total_loss,global_step):
	# num_batches_per_epoch = NUM_EXAMPLES_PER_EPOCH_FOR_TRAIN /BATCH_SIZE
	# decay_steps = int(num_batches_per_epoch * NUM_EPOCHS_PER_DECAY)
	# lr=tf.train.exponential_decay(INITIAL_LEARNING_RATE,
								# global_step,
								# 1000,
								# LEARNING_RATE_DECAY_FACTOR,
								# staircase=True)
	# #loss_averages_op=_add_loss_summaries(total_loss)
	# #with tf.control_dependencies([loss_averages_op]):
	# #	opt=tf.train.GradientDescentOptimizer(lr)
	# #	grads=opt.compute_gradients(total_loss)
	# opt=tf.train.GradientDescentOptimizer(lr)
	# grads=opt.compute_gradients(total_loss)
	# apply_gradient_op=opt.apply_gradients(grads, global_step=global_step)
	
	# variable_averages = tf.train.ExponentialMovingAverage(  										#初始化一个滑动平均操作
		# MOVING_AVERAGE_DECAY, global_step)  
	# variables_averages_op = variable_averages.apply(tf.trainable_variables())  						#将滑动平均操作应用在所有可训练的变量上
	# with tf.control_dependencies([apply_gradient_op, variables_averages_op]):  
		# train_op = tf.no_op(name='train')  															#tf.no_op貌似就是 什么都不做。这样做的目的应该是让apply_gradient_op, variables_averages_op都执行完后，再return
	
	# return train_op
	if(global_step%25==0):
		global INITIAL_LEARNING_RATE
		INITIAL_LEARNING_RATE*=LEARNING_RATE_DECAY_FACTOR
		INITIAL_LEARNING_RATE*=(1-INITIAL_LEARNING_RATE)*0.05
		#print("learning_rate:%0.20f"%INITIAL_LEARNING_RATE)
	return tf.train.AdamOptimizer(INITIAL_LEARNING_RATE).minimize(total_loss)

###################################################################
# def evel_inputs(eval_data_bool):
# 	filepath_list=[FLAGS.TFdata_dir]
# 	for file_path in filepath_list:
# 		if not os.path.exists(file_path):
# 			raise Exception('No such file path'+file_path)
# 	return mycifar10_input.inputs()

###################################################################
def prepare_datadict(train_or_evel):									#准备所有的数据
		
	data_path=os.path.join(FLAGS.image_data_path,train_or_evel)
	if not os.path.exists(data_path):
		raise Exception("Please provide a exist photo datapath")
	dict={}
	label_list=[]
	for label_name in os.listdir(data_path):
		dict[label_name] = [[], 0]
		data_label_path = os.path.join(data_path, label_name)
		for image_name in os.listdir(data_label_path):
			dict[label_name][0].append(image_name)
		dict[label_name][1] = len(dict[label_name][0])
		my_label_insert(label_list,label_name)
	global NUM_CLASSES,BATCH_SIZE
	NUM_CLASSES=len(label_list)
	BATCH_SIZE=FLAGS.batch_size
	return dict,label_list

###################################################################
def distorted_inputs(dict,label_list,train_or_evel):					#抽取BATCH_SIZE数量的图片 作一个集合
	data_path = os.path.join(FLAGS.image_data_path, train_or_evel)
	images=[]
	labels=[]
	label_list_len=len(label_list)
	curr_num=0
	while curr_num<BATCH_SIZE:
		label_random=random.randint(0,label_list_len-1)
		label=label_list[label_random]
		label_path = os.path.join(data_path, label)
		index = random.randint(0, dict[label][1] - 1)
		image_name = dict[label][0][index]
		im_path = os.path.join(label_path, image_name)
		img = Image.open(im_path)
		img = img.resize((FLAGS.photo_resize,FLAGS.photo_resize))
		# img = tf.cast(img, tf.float32) * (1. / 255) - 0.5
		# print(img)
		#img.show()
		images.append(numpy.asarray(img)/255)
		labels.append(label_random)
		curr_num+=1
	return images,labels

###################################################################
def cope_judgeimage(image_path_list):
	images=[]
	for image_path in image_path_list:
		img=Image.open(image_path)
		img=img.resize((FLAGS.photo_resize,FLAGS.photo_resize))
		images.append(numpy.asarray(img)/255)
	return images
	
def my_label_insert(label_list,a):
	length=len(label_list)
	if length==0:
		label_list.append(a)
		return 
	for i in range(length):
		if label_list[i]>a:
			label_list.insert(i,a)
			break
	label_list.insert(i,a)

def setBATCH_SIZE_and_NUM_CLASSES_and_get_label_list(n=1):
	global BATCH_SIZE,NUM_CLASSES
	BATCH_SIZE=n
	
	if not os.path.exists(FLAGS.image_data_path):
		raise Exception("Please provide a exist photo datapath")
	photo_path=os.path.join(FLAGS.image_data_path,'Train')
	label_list=[]
	for label_name in os.listdir(photo_path):
		my_label_insert(label_list,label_name)
	NUM_CLASSES=len(label_list)
	return label_list