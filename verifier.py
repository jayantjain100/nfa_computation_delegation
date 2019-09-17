from nfa import NFA
import socket
from socket_sending import receive_object 
from socket_sending import send_object
import argparse

def verify_ans(given_label, final_labels):
	if(given_label in final_labels):
		return True
	else:
		return False

parser = argparse.ArgumentParser(description='client that delegates NFA computation to prover and verifies')
parser.add_argument('--ip', metavar='ip', type=str, default='127.0.0.1',
					 help='the ip address of the server where the prover is running, default is localhost')
parser.add_argument('--port', metavar = 'port', type = int, default = 12345, help='port number of server to connect to, default is 12345 ')

args = parser.parse_args()

def invoke_verifier(nfas, input_string, indexes):
	# my_nfa = NFA(3, ['a', 'b'], {'a': {0:[1]}, 'b':{1:[2]}} , [2], 0)
	# my_nfa = NFA(4, ['a', 'b'], {'a': {1:[2]}, 'b':{2:[3]}, 'eps':{0:[1], 3:[1]}} , [3], 0)
	# my_nfa = NFA(5, ['a', 'b'], {'a':{0:[1,2], 4:[3]}, 'b':{0:[3], 1:[1,4]}, 'eps':{2:[3,1], 3:[2]}}, [4])
	# 'abababbbbbbbbbbbbbbbbbbbbbbbbbbbbbbba'
	# garble_nfa
	to_send = []
	corresponding_final_labels = []
	for ind in indexes:
		my_nfa = nfas[ind]
		(gnfa, final_labels) = my_nfa.garble(input_string)
		to_send.append(gnfa)
		corresponding_final_labels.append(final_labels)

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# port = 45000
	s.connect((args.ip, args.port))


	#create nfa

	send_object(s, to_send)

	# while True:
	# 	pass	
	received_ans = receive_object(s)

	final_ans = []
	for ind in range(len(received_ans)):
		ans = received_ans[ind]
		if(not ans[0]):		# no, but unsure
			final_ans.append(False)
		elif(ans[0] and verify_ans(ans[1], corresponding_final_labels[ind])):		# yes, confirmed
			final_ans.append(True)
		else:	# wrong proof
			final_ans.append(False)

	return final_ans
