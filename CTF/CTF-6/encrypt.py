import string

START = ord("a")
CHARSET = string.ascii_lowercase[:16]

def decode_b16(b16):
	decoded = ""
	for i in range(0, len(b16), 2):
		binary = "{0:04b}{1:04b}".format(ord(b16[i]) - START, ord(b16[i+1]) - START)
		decoded += (chr(int(binary, 2)))
	return decoded

def encode_b16(plain):
	encoded = ""
	for c in plain:
		binary = "{0:08b}".format(ord(c))
		encoded += (CHARSET[int(binary[:4], 2)] + CHARSET[int(binary[4:], 2)])
	return encoded

def caesar_shift(c, k):
	return CHARSET[(ord(c) + ord(k) - 2 * START) % len(CHARSET)]



enc = open("cipher.txt", "r").readline()
for key in CHARSET:
	dec = ""
	for i, c in enumerate(enc):
		dec += caesar_shift(c, key[i % len(key)])
	decrypted = decode_b16(dec)
	print(decrypted)
