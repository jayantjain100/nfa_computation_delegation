
def encrypt(m,k):
	#both are byte strings
	return m+k

def hash_func(b):
	return b

def decrypt(e, k, hashes):
	ans = e[0:(len(e)-len(k))]
	if hash_func(ans) in hashes:
		return (True, ans)
	else:
		return (False, None)