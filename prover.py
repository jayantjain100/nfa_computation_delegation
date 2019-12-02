"""	Contains the codebase for an honest prover implemeting a Breadth First Search (BFS) """
from nfa import NFA
import socket
from socket_sending import receive_object 
from socket_sending import send_object 
from encryption import encrypt
from encryption import decrypt
from encryption import hash_func
import argparse

parser = argparse.ArgumentParser(description='server that computes encoded NFAs')
parser.add_argument('--port', metavar = 'port', type = int, default = 12345, help='port number, default is 12345')
args = parser.parse_args()

def compute(gt, hashes, final_hashes, start_label):
	"""Performs BFS over given garbled NFA and returns a tuple implying if the string is accepted in the NFA or not.
	Takes input the garbled NFA (The garbled tables: gt, hashes of the final states: final_hashes, label for the start state: start_label)
	returns a tuple (a,b) s.t. if input string is accepting in the NFA then a=True and b=(label of the final state reached) else a=False and b=None"""

	# create frontier 0 using gt_0 and start_label
	current_frontier = [start_label]
	while(True):
		flag = False
		keys = [(label) for label in current_frontier]
		for k in keys:
			for e in gt[0]:
				(success, ans) = decrypt(e, k, hashes[0])
				if(success and (ans not in current_frontier)):
					current_frontier.append(ans)
					flag = True

		if(not flag):
			break

	# now interatively given the current frontier and gt_i find the next_frontier
	for i in range(1, len(gt)):
		next_frontier = []
		keys = [(label) for label in current_frontier]

		for k in keys:
			for e in gt[i]:
				(success, ans) = decrypt(e,k, hashes[i])
				if(success and (ans not in next_frontier)):
					next_frontier.append(ans)

		# we have the direct labels in next_frontier, now take epsilon closure
		while True:
			flag = False
			keys = [(label) for label in next_frontier]
			for k in keys:
				for e in gt[i]:
					(success, ans) = decrypt(e,k, hashes[i])
					if(success and (ans not in next_frontier)):
						next_frontier.append(ans)
						flag = True
			if (not flag):
				break

		current_frontier = next_frontier

	# after all loops we have the final frontier
	obtained_hashes = [hash_func(label) for label in current_frontier]
	for i in range(len(obtained_hashes)):
		for h in final_hashes:
			if obtained_hashes[i] == h:
				return (True, current_frontier[i])

	return(False, None)

if __name__ == '__main__':
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		# port = 12345
	s.bind(('', args.port))
	#empty strings means that accepts connections from everywhere
	s.listen(10)

	while(True):
		#connect to one person, receive multiple queries in a list, answer them and disconnect
		c, addr = s.accept()	 
		print ('Got connection from', addr) 
		# recieve garbled input
		gnfas = receive_object(c)
		print('recieved garbled nfas from Verifier' )
		to_send = []
		for gnfa in gnfas:
			ans = compute(gnfa[0], gnfa[1], gnfa[2], gnfa[3])
			# send a thank you message to the client.
			dict1 = {True:'Accepting', False:'Not Accepting'} 
			print('prover computed', dict1[ans[0]] )
			to_send.append(ans)	
		send_object(c, to_send) 
	# Close the connection with the client 
	c.close() 

