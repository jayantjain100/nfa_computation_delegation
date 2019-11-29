from nfa import NFA
# from prover import invoke_prover
from verifier import invoke_verifier
from regex import regex_to_nfa
import numpy as np
import copy
import sys

NUM_TRIALS = 2

if __name__ == '__main__':
	
	regex = input('Enter the regex describing the NFA: ')
	input_string = input('Enter the input string: ')
	my_nfa = regex_to_nfa(regex)
	# my_nfa = NFA(3, ['a', 'b'], {'a': {0:[1]}, 'b':{1:[2]}} , [2], 0)
	my_nfa.complete()
	known_nfa = my_nfa.get_similar_nfa(input_string)
	indexes = [0 for i in range(NUM_TRIALS)] + [1 for i in range(NUM_TRIALS)]
	
	# shuffling of indexes of known and unknown problems
	arr = (np.array(indexes))
	np.random.shuffle(arr)
	indexes = list(arr)
	
	answers = invoke_verifier([my_nfa, known_nfa], input_string, indexes)
	
	seems_trustworthy = True
	ans_is_yes = False
	for ind in range(len(indexes)):
		if (indexes[ind]==1 and (not answers[ind])):
			seems_trustworthy = False
		elif (indexes[ind]==0 and answers[ind]):
			ans_is_yes = True

	if((not seems_trustworthy) and ans_is_yes):
		print("Gave wrong answer for the known problem!, but confirmed YES for actual problem")
	elif(not seems_trustworthy):
		print("Gave wrong answer for known problem!")
	elif(ans_is_yes):
		print("Verified the answer as YES")
	else:
		print("Verified the answer as NO")
