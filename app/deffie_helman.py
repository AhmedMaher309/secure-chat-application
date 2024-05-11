import random

class DeffieHellman:
	def __init__(self):
		self.p , self.g = self.generate_P_and_G()
		self.save_P_and_G("DH.txt")
		
	def prime_checker(self, p):
		# Checks If the number entered is a Prime Number or not
		if p < 1:
			return -1
		elif p > 1:
			if p == 2:
				return 1
			for i in range(2, p):
				if p % i == 0:
					return -1
				return 1


	def primitive_check(self, g, p, L):
		# Checks If The Entered Number Is A Primitive Root Or Not
		for i in range(1, p):
			L.append(pow(g, i) % p)
		for i in range(1, p):
			if L.count(i) > 1:
				L.clear()
				return -1
			return 1

	def generate_P_and_G(self, min_range=1, max_range=30, bits=128):
		while True:
			# Generate a random prime number within the specified range
			p = random.randint(min_range, max_range)
			if self.prime_checker(p) == 1:
				# Generate a random generator (g) for the prime (p)
				g = random.randint(2, p - 1)
				L = []
				if self.primitive_check(g, p, L) == 1:
					return p, g


	def save_P_and_G(self, file_path):
		# Save p and g to separate lines in the same file
		with open(file_path, "w") as file:
			file.write(str(self.p) + "\n")
			file.write(str(self.g))

