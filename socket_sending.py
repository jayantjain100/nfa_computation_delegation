""" Contains functions for sending and receiving objects using sockets """
import socket
import pickle

PACKET_SIZE = 1024
HEADERSIZE = 10
 
def receive_object(s):
	# waits for receiving the input from alice
	stream = b''
	new_msg = True
	while(True):
		received = s.recv(PACKET_SIZE)
		if(new_msg):
			new_msg = False
			byte_length = int(received[:HEADERSIZE])
		
		if(len(received)==0):
			# indicates closed connection
			# but we don't want to break only if the connection closes
			# we shall also break when we've fully read the header
			print("lost connection, closing receive")
			break

		stream += received

		if len(stream)-HEADERSIZE == byte_length:
			#ideal break
			break

	obj =  pickle.loads(stream[HEADERSIZE:])	
	return obj

def send_object(other_socket, obj):
	byte_obj = pickle.dumps(obj)
	header = bytes(f"{len(byte_obj):<{HEADERSIZE}}", 'utf-8')
	other_socket.send(header + byte_obj)
	