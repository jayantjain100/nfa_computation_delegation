# testing.py
from nfa import NFA
import socket
from socket_sending import receive_object 
from socket_sending import send_object 
from encryption import encrypt
from encryption import decrypt
from encryption import hash_func

def compute(gt, hashes, final_hashes, start_label):
	#isko bas ek input milta hai at a time and yeh uske sath deal karke ans bhejta hai
	#honest algo

	#create frontier 0 using gt_0 and start_label
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

	#now interatively given the current frontier and gt_i i want to find the next_frontier
	#breadth first search in search space

	for i in range(1, len(gt)):
		next_frontier = []
		keys = [(label) for label in current_frontier]

		for k in keys:
			for e in gt[i]:
				(success, ans) = decrypt(e,k, hashes[i])
				if(success and (ans not in next_frontier)):
					next_frontier.append(ans)

		#now i have my direct labels in next_frontier , now take epsilon closure
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

	#after all loops i have the final frontier

	obtained_hashes = [hash_func(label) for label in current_frontier]
	for i in range(len(obtained_hashes)):
		for h in final_hashes:
			if obtained_hashes[i] == h:
				return (True, current_frontier[i])

	return(False, None)



# my_nfa = NFA(3, ['a', 'b'], {'a': {0:[1]}, 'b':{1:[2]}} , [2], 0)
my_nfa = NFA(5, ['a', 'b'], {'a':{0:[1,2], 4:[3]}, 'b':{0:[3], 1:[1,4]}, 'eps':{2:[3,1], 3:[2]}}, [4])

#garble_nfa
(gnfa, final_labels) = my_nfa.garble('ab', 3)

ans = compute(gnfa[0], gnfa[1], gnfa[2], gnfa[3])