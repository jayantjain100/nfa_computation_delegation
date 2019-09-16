import os
import base64
import cryptography
import hashlib
# Available algorithms are 'sha256', 'sha384', 'sha224', 'sha512', 'sha1', 'md5'
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

salt = b"\xb9\x1f|}'S\xa1\x96\xeb\x154\x04\x88\xf3\xdf\x05"

def hash_func(b):
	return hashlib.sha256(b).digest()

def encrypt(message: bytes, key: bytes) -> bytes:
	kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=100000,backend=default_backend())
	return Fernet(base64.urlsafe_b64encode(kdf.derive(key))).encrypt(message)

def decrypt(token: bytes, key: bytes, my_hashes) -> bytes:
	kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=100000,backend=default_backend())
	try:
		f = Fernet(base64.urlsafe_b64encode(kdf.derive(key))).decrypt(token)
		if hash_func(f) in my_hashes:
			return (True, f)
		return (False, None)
	except cryptography.fernet.InvalidToken:
		return (False, None)
