import socket
import pickle

PACKET_SIZE = 1024
HEADERSIZE = 10

def receive_object(s):
	# print('enter')
	#waits for receiving the input from alice
	#return the input 
	stream = b''
	new_msg = True
	# started = False
	while(True):
		received = s.recv(PACKET_SIZE)
		if(new_msg):
			new_msg = False
			byte_length = int(received[:HEADERSIZE])
		
		if(len(received)==0):
			#indicates closed connection
			#but i dont want to break only if the connection closes
			#i shall break when ive fully read my header
			print("lost connection, closing receive")
			break

		stream += received

		if len(stream)-HEADERSIZE == byte_length:
			#ideal break
			break

	# print('byte object is ', stream)
	obj =  pickle.loads(stream[HEADERSIZE:])	
	# print('exit')
	return obj

def send_object(other_socket, obj):
	byte_obj = pickle.dumps(obj)
	header = bytes(f"{len(byte_obj):<{HEADERSIZE}}", 'utf-8')
	other_socket.send(header + byte_obj)
	# num_packets = int((len(byte_obj) + PACKET_SIZE - 1)/(PACKET_SIZE))
	# for i in range(num_packets):
	# 	other_socket.send(byte_obj[i*PACKET_SIZE : min(((i+1)*PACKET_SIZE-1),len(byte_obj)-1)])
	