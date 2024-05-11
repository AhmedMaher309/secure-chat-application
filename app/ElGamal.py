import random

class ElGamal:
	def __init__(self):
		self.q , self.a = self.generate_q_and_a()
		self.save_q_and_a("gamal.txt")
		
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

	def generate_q_and_a(self, min_range=1, max_range=500, bits=128):
		while True:
			# Generate a random prime number within the specified range
			q = random.randint(min_range, max_range)
			if self.prime_checker(q) == 1:
				# Generate a random generator (g) for the prime (p)
				a = random.randint(2, q - 1)
				L = []
				if self.primitive_check(a, q, L) == 1:
					return q, a


	def save_q_and_a(self, file_path):
		# Save p and g to separate lines in the same file
		with open(file_path, "w") as file:
			file.write(str(self.q) + "\n")
			file.write(str(self.a))

