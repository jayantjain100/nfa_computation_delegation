
class nfa:
	def __init__(self, 
				num_states,
				alphabet, 
				delta, 
				epsilon_trans,
				final_states, 
				start_state = 0):

		#num_states is the number of states the nfa has labelled as 0,1....(num_states -1)
		#alphabet is a list of characters excluding epsilon(SIGMA)
		#delta is the transitions addressed as delta[char][state] = next_state
		#final_states is a list of accepting states
		#start state is just the state to start from and if not given is considered 0

		#we add a dump state khud for all undefined transitions
		self.num_states = num_states + 1
		self.alphabet = alphabet
		for char in alphabet:
			self.delta[char] = [(self.num_states-1) for i in range(self.num_states)]
			#self goes to dump shuru mei
		#now use the given transitions to include the actual meaningful transitions
		#self.delta is a hash that maps characters to all jumps (complete)
		#delta maps charcters to a map of states to jumps(incomplete)
		for char in delta:
			for i in delta[char]:
				self.delta[char][i] = delta[char][i]

		#map between state1 that can jump to state2 with epsilon
		#keeping separate will be easier
		self.epsilon_trans = epsilon_trans

		self.final_states = final_states
		self.start_state = start_state