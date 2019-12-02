""" Contains the codebase for a verifier who takes a regex and an input string over some alphabet and delegates the 
	problem along with a similar problem with a known 'YES' answer to gain trust.
	- Takes the regex, makes an NFA out of it, creates an NFA with similar "structure" which accepts the input string,
	  delegates both the actual and known problem NUM_TRIALS times, gains trust using the answers for the known problems 
	  and tries to verify the answer to the actual problem with high probability.
"""
from nfa import NFA
from delegate import delegate
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

	# a list of NUM_TRIALS 0's and NUM_TRIALS 1's s.t. each 0 represents the actual problem and 1 represents the known problem
	indexes = [0 for i in range(NUM_TRIALS)] + [1 for i in range(NUM_TRIALS)]
	
	# shuffling of indexes of known and unknown problems
	arr = (np.array(indexes))
	np.random.shuffle(arr)
	indexes = list(arr)
	
	# Delegate the problem and receive the answers to all the problems sent
	answers = delegate([my_nfa, known_nfa], input_string, indexes)
	
	# Check if the answer to all the instances of known problem is YES and verify them
	seems_trustworthy = True
	ans_is_yes = False
	for ind in range(len(indexes)):
		if (indexes[ind]==1 and (not answers[ind])):
			seems_trustworthy = False
		elif (indexes[ind]==0 and answers[ind]):
			ans_is_yes = True

	# If prover seems to be trustworthy then assume the answer received for the actual problem to be correct
	if((not seems_trustworthy) and ans_is_yes):
		print("Gave wrong answer for the known problem!, but confirmed YES for actual problem")
	elif(not seems_trustworthy):
		print("Gave wrong answer for known problem!")
	elif(ans_is_yes):
		print("Verified the answer as YES")
	else:
		print("Verified the answer as NO")
