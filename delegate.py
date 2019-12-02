from nfa import NFA
import socket
from socket_sending import receive_object 
from socket_sending import send_object
import argparse

def verify_yes_ans(given_label, final_labels):
	if(given_label in final_labels):
		return True
	else:
		return False

parser = argparse.ArgumentParser(description='client that delegates NFA computation to prover and verifies')
parser.add_argument('--ip', metavar='ip', type=str, default='127.0.0.1',
					 help='the ip address of the server where the prover is running, default is localhost')
parser.add_argument('--port', metavar = 'port', type = int, default = 12345, help='port number of server to connect to, default is 12345 ')

args = parser.parse_args()

def delegate(nfas, input_string, indexes):
	to_send = []
	corresponding_final_labels = []
	print('Creating garbled NFAs...')
	for ind in indexes:
		my_nfa = nfas[ind]
		(gnfa, final_labels) = my_nfa.garble(input_string)
		to_send.append(gnfa)
		corresponding_final_labels.append(final_labels)

	print('Sending garbled NFAs...')
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# port = 45000
	s.connect((args.ip, args.port))

	send_object(s, to_send)

	print('Waiting to receive result from prover...')
	received_ans = receive_object(s)
	print('Received the result.!')
	print()

	final_ans = []
	for ind in range(len(received_ans)):
		ans = received_ans[ind]
		if(not ans[0]):		# no, but unsure
			final_ans.append(False)
		elif(ans[0] and verify_yes_ans(ans[1], corresponding_final_labels[ind])):		# yes, confirmed
			final_ans.append(True)
		else:	# wrong proof given by prover
			final_ans.append(False)

	return final_ans
