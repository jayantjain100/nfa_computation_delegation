""" Contains the NFA class for description of NFAs using states: 0 to (num_states-1), the alphabet: alphabet, transition function: delta
	set of final states: final_states and start_state.
	Contains methods (i) complete() for getting complete description (a transition is defined for each character from each of the states) of the NFA from a partial description (with no transtion on certain characters)
			   	     (ii) get_similar_nfa() for getting an NFA with similar "stricture" with answer YES on the given input
 					 (iii) garble() for getting a garbled representation of the NFA 
 """
from encryption import hash_func
from encryption import encrypt
from encryption import decrypt
import os
import numpy as np
from cryptography.fernet import Fernet
import random

class NFA:
	def __init__(self,
				num_states,
				alphabet,
				delta,
				final_states,
				start_state = 0):
		# considering sparse representation
		# an undefined transition implies rejection of string (going to a non accepting dump which loops to itslef for all input)

		self.num_states = num_states 
		self.alphabet = alphabet

		# Transitions description
		"""eg = {'a':{1:[3,4] , 3:[2,1]}, 'c':{2:[0]}, 'eps':{0:[1,2,3,4]}} this is the form of delta
		it is a dictionary which maps chars to the tables of transitions that happen on that specific char
		here each table maps prev to possible_nexts"""

		# specifying an empty entry in the description as delta[c] = {} for all characters c in the alphabet
		true_alphabet = delta.keys()
		for char in alphabet:
			if (char not in true_alphabet):
				delta[char] = {}
		
		if('eps' not in true_alphabet):
			delta['eps'] = {}

		self.delta = delta
		self.final_states = final_states
		self.start_state = start_state

	def complete(self):
		# Add a dump state and for all characters for which no transition is defined for a state...
		# add a transition from it to the dump state on that character
		self.num_states += 1
		for char in self.alphabet:
			temp = { i:[(self.num_states-1)] for i in range(self.num_states)}
			for k in self.delta[char]:
				temp[k] = self.delta[char][k]
			self.delta[char] = temp

	def get_similar_nfa(self, input_string):
		# Get an NFA (similar to the self NFA) that accepts the given input string (ends in a final state on input_string)
		current = self.start_state
		for i in range(len(input_string)):
			char_of_interest = input_string[i]
			possible_nexts =  self.delta[char_of_interest][current]
			current = random.choice(possible_nexts)
			if current in self.delta['eps'].keys():
				possible_nexts = (self.delta['eps'][current]) + [current]
				current = random.choice(possible_nexts)

		new_final_states = [current]
		return NFA(self.num_states, self.alphabet, self.delta, new_final_states, self.start_state)

	def garble(self, input_string, security_param = 32):
		""" produces the garbling corresponding to the NFA and input string
		therefore returns ((garbled_tables, hashes, final_hashes),(L_l of F for the verifier to confirm)) """
		input_len = len(input_string)
		# l is inpu_len
		# l+1 encodings where each encodes all states
		L = [[os.urandom(security_param) for j in range(self.num_states)] for i in range(input_len + 1)]

		#both are list of lists
		garbled_tables = [] #l+1 tables exist
		hashes = [] #l+1 lists exist


		for i in range(input_len+1):
			present_table = []
			present_hashes = []
			unlockable = []

			if(i != 0):
				char_of_interest = input_string[i-1]
				for prev in self.delta[char_of_interest]:
					lis_of_next = self.delta[char_of_interest][prev]
					for succ in lis_of_next:
						#include (prev, next ) in gt
						info = L[i][succ]
						key = (L[i-1][prev])
						# key = hash_func1(L[i-1][prev])
						present_table.append(encrypt(info, key))

						if succ not in unlockable:
							unlockable.append(succ)
							present_hashes.append(hash_func(L[i][succ]))

			#now including all epsilon transitions
			for prev in self.delta['eps']:
				lis_of_next = self.delta['eps'][prev]
				for succ in lis_of_next:
					#include (prev, next ) in gt
					info = L[i][succ]
					key = (L[i][prev]) #we have same label here ab
					# key = hash_func1(L[i][prev]) #we have same label here ab
					present_table.append(encrypt(info, key))

					if succ not in unlockable:
						unlockable.append(succ)
						present_hashes.append(hash_func(L[i][succ]))

			#Now that we have present table and present hashes include these in our ans
			arr = (np.array(present_table))
			np.random.shuffle(arr)
			present_table = list(arr)
		
			garbled_tables.append(present_table)
			hashes.append(present_hashes)

		#now create final_hashes, and final_labels
		final_labels = [ L[input_len][f] for f in self.final_states]
		final_hashes = [hash_func(label) for label in final_labels ]

		return ((garbled_tables, hashes, final_hashes, L[0][self.start_state]), (final_labels))


	# def compute(self, string):
	# 	return True