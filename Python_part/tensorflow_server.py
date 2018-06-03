#import time
import threading
import socket
import json

from MyCNN import plr

#def test(str):
#	print("thread %s is running...%s"%(threading.current_thread().name,str))
#	time.sleep(2)
#	print("thread %s has ended"%threading.current_thread().name)

#str1="D:/tmp/book/photo.jpg"
#str2="D:/fuck/you/xxxx.jpg"
#thread1=threading.Thread(target=test,args=(str1,))
#thread2=threading.Thread(target=test,args=(str2,))
#thread1.start()
#thread2.start()

bind_ip='127.0.0.1'
bind_port=6666

def tcplink(client_sock,client_addr):
	print('Accept new connection from %s:%s...' % client_addr)
	photo_path=(client_sock.recv(256)).decode('utf-8')
	# print("client:%s"%photo_path)
	character,label=plr.input_photo(photo_path)
	#调用 Tensorflow...
	#label="book"
	result=json.dumps({"character":character,"label":label})					#将图片特征值和便签名传输过去
	client_sock.send(result.encode('utf-8'))
	client_sock.close()
	print('Connection from %s:%s closed.' % client_addr)

if __name__=='__main__':
	plr.init_tensorflow()			#初始化Tensorflow
	server_sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_sock.bind((bind_ip,bind_port))
	server_sock.listen(10)
	print("TensorflowServer is waiting for connection")

	while True:
		client_sock,client_addr=server_sock.accept()
		mythread=threading.Thread(target=tcplink,args=(client_sock,client_addr))
		mythread.start()
