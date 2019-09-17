from nfa import NFA
# from prover import invoke_prover
from verifier import invoke_verifier
import numpy as np

NUM_TRIALS = 1

if __name__ == '__main__':
	
	# invoke_prover()
	my_nfa = NFA(5, ['a', 'b'], {'a':{0:[1,2], 4:[3]}, 'b':{0:[3], 1:[1,4]}, 'eps':{2:[3,1], 3:[2]}}, [4])
	input_string = 'abababbbbbbbbbbbbbbbbbbbbbbbbbbbbbbba'
	# known_nfa = my_nfa.get_similar_nfa(input_string)
	known_nfa = my_nfa

	indexes = [0 for i in range(NUM_TRIALS)] + [1 for i in range(NUM_TRIALS)]

	# shuffling of indexes of known and unknown problems
	arr = (np.array(indexes))
	np.random.shuffle(arr)
	indexes = list(arr)
	
	answers = invoke_verifier([my_nfa, known_nfa], input_string, indexes)
	# print("answers: ", answers)

	seems_trustworthy = True
	ans_is_yes = False
	for ind in range(len(indexes)):
		if (indexes[ind]==1 and (not answers[ind])):
			seems_trustworthy = False
		elif (indexes[ind]==0 and answers[ind]):
			ans_is_yes = True

	# print("seems_trustworthy: ", seems_trustworthy) 
	# print("ans_is_yes: ", ans_is_yes) 

	if((not seems_trustworthy) and ans_is_yes):
		print("Gave wrong answer for the known problem!, but confirmed YES for actual problem")
	elif(not seems_trustworthy):
		print("Gave wrong answer for known problem!")
	elif(ans_is_yes):
		print("Verified the answer as YES")
	else:
		print("Verified the answer as NO")
