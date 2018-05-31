import tensorflow as tf
import os
import random
import numpy
from PIL import Image

#import mycifar10_input
FLAGS=tf.app.flags.FLAGS
tf.app.flags.DEFINE_string('image_data_path','D:/tmp/mycifar10_data',
						   """The path of image""")
tf.app.flags.DEFINE_integer('photo_resize',16,						##s:32
							"""resize the photo""")
# tf.app.flags.DEFINE_string('TFdata_dir','D:/tmp/mycifar10_data/TFRecords',
# 							"""Path to the photo(TFRecords) data directory.""")
# tf.app.flags.DEFINE_integer('save_photo_size',224,
# 							"""TFRecords save photo size.""")				#生成TFRecords文件时，按照这个尺寸存放图片

global NUM_CLASSES,BATCH_SIZE
NUM_EXAMPLES_PER_EPOCH_FOR_TRAIN=300

NUM_EPOCHS_PER_DECAY=350.0
LEARNING_RATE_DECAY_FACTOR=0.01
INITIAL_LEARNING_RATE=0.1
MOVING_AVERAGE_DECAY=0.9999
							
# def train_distorted_inputs():
# 	filepath_list=[os.path.join(FLAGS.TFdata_dir,'Train.tfrecords')]
# 	for file_path in filepath_list:
# 		if not os.path.exists(file_path):
# 			raise Exception('No such file path'+file_path)
# 	return mycifar10_input.distorted_inputs(filepath_list)
	
###################################################################		

# def _create_TFRecords(photo_path):
# 	def create(photo_path,isTrain=True):
# 		if not os.path.exists(photo_path):
# 			raise Exception("Please provide a exist photo datapath")
# 		choose='Train'
# 		label_writer=None
# 		if not isTrain:
# 			choose='Evel'
# 		photo_path=os.path.join(photo_path,choose)
# 		writer=tf.python_io.TFRecordWriter(os.path.join(FLAGS.TFdata_dir,choose+".tfrecords"))
# 		index=0
# 		for label in os.listdir(photo_path):
# 			label_path=os.path.join(photo_path,label,'full')
# 			for img_name in os.listdir(label_path):
# 				img_path=os.path.join(label_path,img_name)
# 				img=Image.open(img_path)
# 				img=img.resize((FLAGS.save_photo_size,FLAGS.save_photo_size))			#改变图片尺寸
# 				img_raw=img.tobytes()        #将图片转化为原生bytes
# 				example=tf.train.Example(features=tf.train.Features(feature={
# 					"label": tf.train.Feature(int64_list=tf.train.Int64List(value=[index])),
# 					'img_raw': tf.train.Feature(bytes_list=tf.train.BytesList(value=[img_raw]))
# 				}))
# 				writer.write(example.SerializeToString())		#序列化为字符串
# 			index+=1
# 		writer.close()
#
# 	TFpath=FLAGS.TFdata_dir
# 	os.mkdir(TFpath)
# 	create(photo_path,isTrain=True)
# 	create(photo_path,isTrain=False)
#
# def check_or_create_TFRecords():
# 	photo_path='D:/tmp/mycifar10_data'
# 	if not os.path.exists(FLAGS.TFdata_dir):
# 		_create_TFRecords(photo_path)
# 	#NUM_CLASSES=len(os.listdir(os.path.join(photo_path,'Evel')))
# 	#print("????"+str(NUM_CLASSES)+"?????")
		
###################################################################

def _variable_on_cpu(name,shape,initializer):
	with tf.device('/cpu:0'):
		var =tf.get_variable(name,shape,initializer=initializer)
	return var

def _variable_with_weight_decay(name, shape,stddev,wd):
	var = _variable_on_cpu(name,shape,
						tf.truncated_normal_initializer(stddev=stddev))
	if wd:
		weight_decay=tf.multiply(tf.nn.l2_loss(var),wd,name='weight_loss')
		tf.add_to_collection('losses',weight_decay)
	return var

def inference(images):
	# local3
	with tf.variable_scope('local3') as scope:
		dim=1
		for d in images.get_shape()[1:].as_list():
			dim*=d
		reshape=tf.reshape(images,[BATCH_SIZE,dim])
		weights=_variable_with_weight_decay('weights',shape=[dim,384],					#384
										stddev=0.04,wd=0.004)
		biases=_variable_on_cpu('biases',[384],tf.constant_initializer(0.1))
		local3=tf.nn.relu(tf.matmul(reshape,weights)+biases,name=scope.name)
		#_activation_summary(local3)
	# local4	
	with tf.variable_scope('local4') as scope:  
		weights = _variable_with_weight_decay('weights', shape=[384, 192],  
											stddev=0.04, wd=0.004)  
		biases = _variable_on_cpu('biases', [192], tf.constant_initializer(0.1))  
		local4 = tf.nn.relu(tf.matmul(local3, weights) + biases, name=scope.name)  
		#_activation_summary(local4)  
	# softmax, i.e. softmax(WX + b)  
	with tf.variable_scope('softmax_linear') as scope:  
		weights = _variable_with_weight_decay('weights', [192, NUM_CLASSES],  
											  stddev=1/192.0, wd=0.0)  
		biases = _variable_on_cpu('biases', [NUM_CLASSES],  
								  tf.constant_initializer(0.0))  
		softmax_linear = tf.add(tf.matmul(local4, weights), biases, name=scope.name)  
		#_activation_summary(softmax_linear)  
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
	tf.add_to_collection('losses',cross_entropy_mean)
	
	return tf.add_n(tf.get_collection('losses'),name='total_loss')
	
###################################################################

def _add_loss_summaries(total_loss):
	loss_averages=tf.train.ExponentialMovingAverage(0.9,name='avg')
	losses=tf.get_collection('losses')
	loss_averages_op=loss_averages.apply(losses+[total_loss])
	
	return loss_averages_op

def train(total_loss,global_step):
	num_batches_per_epoch = NUM_EXAMPLES_PER_EPOCH_FOR_TRAIN /BATCH_SIZE
	decay_steps = int(num_batches_per_epoch * NUM_EPOCHS_PER_DECAY)
	lr=tf.train.exponential_decay(INITIAL_LEARNING_RATE,
								global_step,
								decay_steps,
								LEARNING_RATE_DECAY_FACTOR,
								staircase=True)
	loss_averages_op=_add_loss_summaries(total_loss)
	with tf.control_dependencies([loss_averages_op]):
		opt=tf.train.GradientDescentOptimizer(lr)
		grads=opt.compute_gradients(total_loss)
	apply_gradient_op=opt.apply_gradients(grads, global_step=global_step)
	
	variable_averages = tf.train.ExponentialMovingAverage(  										#初始化一个滑动平均操作
		MOVING_AVERAGE_DECAY, global_step)  
	variables_averages_op = variable_averages.apply(tf.trainable_variables())  						#将滑动平均操作应用在所有可训练的变量上
	with tf.control_dependencies([apply_gradient_op, variables_averages_op]):  
		train_op = tf.no_op(name='train')  															#tf.no_op貌似就是 什么都不做。这样做的目的应该是让apply_gradient_op, variables_averages_op都执行完后，再return
	
	return train_op  

###################################################################
# def evel_inputs(eval_data_bool):
# 	filepath_list=[FLAGS.TFdata_dir]
# 	for file_path in filepath_list:
# 		if not os.path.exists(file_path):
# 			raise Exception('No such file path'+file_path)
# 	return mycifar10_input.inputs()

###################################################################
def prepare_datadict(train_or_evel):
		
	data_path=os.path.join(FLAGS.image_data_path,train_or_evel)
	if not os.path.exists(data_path):
		raise Exception("Please provide a exist photo datapath")
	dict={}
	label_list=[]
	for label_name in os.listdir(data_path):
		dict[label_name] = [[], 0]
		data_label_path = os.path.join(data_path, label_name, 'full')
		for image_name in os.listdir(data_label_path):
			dict[label_name][0].append(image_name)
		dict[label_name][1] = len(dict[label_name][0])
		my_label_insert(label_list,label_name)
	global NUM_CLASSES,BATCH_SIZE
	NUM_CLASSES=len(label_list)
	BATCH_SIZE=FLAGS.batch_size
	return dict,label_list

###################################################################
def distorted_inputs(dict,label_list,train_or_evel):
	data_path = os.path.join(FLAGS.image_data_path, train_or_evel)
	images=[]
	labels=[]
	label_list_len=len(label_list)
	curr_num=0
	while curr_num<BATCH_SIZE:
		label_random=random.randint(0,label_list_len-1)
		label=label_list[label_random]
		label_path = os.path.join(data_path, label, 'full')
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