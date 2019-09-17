#nfa2.py
#pending - make gods nfa for soln to no
#rewiriting from scratch because of certain algo changes
from encryption import hash_func
# from encryption import hash_func2
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
		#do i need to model this as a true nfa, that every transition should be defined?
		#this is just the question of and adjacency list v matrix in graphs

		#considering sparse
		#an undefined transition implies rejection of string (going to a non accepting dump which loops to itslef for all input)

		#have to make gods nfa so that i can actuaaly choose a random path without a problem
		self.num_states = num_states 
		self.alphabet = alphabet

		#eg = {'a':{1:[3,4] , 3:[2,1]}, 'c':{2:[0]}, 'eps':{0:[1,2,3,4]}} this is the form of delta
		#it is a dictionary which maps chars to the tables of transitions that happen on that specific char
		#here each table maps prev to possible_nexts

		#PE - someone specifying an empty entry in the description as in delta[c] = {} pehle se aajaye
		true_alphabet = delta.keys()
		for char in alphabet:
			if (char not in true_alphabet):
				delta[char] = {}
		# for char in alphabet:
		# 	temp = { i:[(self.num_states-1)] for i in range(self.num_states)}
		# 	if (char in true_alphabet):
		# 		for k in delta[char]:
		# 			temp[k] = delta[char][k]
		# 	delta[char] = temp
		if('eps' not in true_alphabet):
			delta['eps'] = {}

		self.delta = delta
		self.final_states = final_states
		self.start_state = start_state

	def complete(self):
		self.num_states += 1
		for char in self.alphabet:
			temp = { i:[(self.num_states-1)] for i in range(self.num_states)}
			for k in self.delta[char]:
				temp[k] = self.delta[char][k]
			self.delta[char] = temp

	def draw(self):
		#calls the graphviz module whith appropriate args
		pass

	def get_similar_nfa(self, input_string):
		current = self.start_state
		for i in range(len(input_string)):
			char_of_interest = input_string[i]
			possible_nexts =  self.delta[char_of_interest][current]
			current = random.choice(possible_nexts)
			#PE , LATER find the epsilon closure and choose something random, for true randomness
			# print(self.delta)
			if current in self.delta['eps'].keys():
				possible_nexts = (self.delta['eps'][current].values()) + [current]
				current = random.choice(possible_nexts)

		new_final_states = [current]
		return NFA(self.num_states, self.alphabet, self.delta, new_final_states, self.start_state)

	def garble(self, input_string, security_param = 32):
		#produces the garbling corresponding to a  
		# therefore returns ((garbled_tables, hashes, final_hashes),(L_l of F for the verifier to confirm))
		input_len = len(input_string)
		#l is inpu_len
		# l+1 encodings where each encodes all states
		L = [[os.urandom(security_param) for j in range(self.num_states)] for i in range(input_len + 1)]

		#both are list of lists
		garbled_tables = [] #l+1 tables hongi
		hashes = [] #l+1 lists hongi	


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

			#now including all epsilon trans
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

			#Now that i have present table and present hashes include these in your ans
			# print(present_table)
			# if present_table != []:
			arr = (np.array(present_table))
			np.random.shuffle(arr)
			present_table = list(arr)
		
			garbled_tables.append(present_table)
			hashes.append(present_hashes)

		#now create final_hashes, and final_labels
		final_labels = [ L[input_len][f] for f in self.final_states]
		final_hashes = [hash_func(label) for label in final_labels ]

		return ((garbled_tables, hashes, final_hashes, L[0][self.start_state]), (final_labels))


	def compute(self, string):
		return True