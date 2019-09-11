# Alice encodes the computation and sends it to BOB
from nfa import nfa
import random 
import hashlib

#abstraction
from encryption import encrypt
from encryption import decrypt
from encryption import hash_func

import os
import numpy as np
#for debugging purposes
random.seed(0)

class garbled_nfa():
	def __init__(self, my_nfa, input_string, security_param= 256):
		self.input_length = len(input_string)
		self.my_nfa = my_nfa  #do i need this

		#start the process
		#refer to doc

		#taking the security parameter as 256 by default
		#create n Label functions L_i
		#bytes form of data
		L = [[os.urandom(security_param) for j in range(self.my_nfa.num_states)] for i in range(self.input_length + 1)]
		#initialised all labels
		# garbled_tables = [[] for i in range(self.input_length)]
		garbled_tables = []
		hashes = []

		for i in range (self.input_length):
			#for all tables
			character = input_string[i]
			present_table = []
			present_hashes = []
			unlockable = []

			for j in range(self.my_nfa.num_states):
				#for each possible jump
				dest = self.my_nfa.delta[character]
				to_encrypt = L[i+1][dest]
				password_for_encryption = L[i][j]
				#because there is a jump from j to dest on the ith char of input string
				
				present_table.append(encrypt(to_encrypt,password_for_encryption))
				
				if dest not in unlockable:
					unlockable.append(dest)
					present_hashes.append(hash_func(to_encrypt))


			#now the original table has been created, now include epsilon transitions
			while True:
				bool exists = False
				for eps_jump in self.my_nfa.epsilon_trans:
					#eps_jump is a key in the hash table
					#it is the left state in the jump
					prev = eps_jump
					succ = self.my_nfa.epsilon_trans[prev]
					if ((prev in unlockable) and (succ not in unlockable)) 
						#this means its a part of the original
						exists = True
						to_encrypt = L[i+1][succ]
						password_for_encryption = L[i+1][prev]
						present_table.append(encrypt(to_encrypt,password_for_encryption))
						unlockable.append(succ)
						present_hashes.append(hash_func(to_encrypt))
				
				if(not exists):
					break

			#shuffle/garble this
			present_table = list((np.array(present_table)).shuffle())
			garbled_tables.append(present_table)
			hashes.append(present_hashes)

		final_state_hashes = [hash_func(L[self.my_nfa.input_length][i])
							  for i in range(self.my_nfa.num_states)
								if (i in self.my_nfa.final_states)]

		self.garbled_tables = garbled_tables
		self.final_state_hashes = final_state_hashes
		self.hashes = hashes



