import random 
import hashlib

class Elgamal:
	
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

    def generate_q_and_a(self, min_range=1, max_range=50, bits=128):
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
    

    def get_m(self, M, max):
        # Calculate the SHA-1 hash of the input number
        sha1_hash = hashlib.sha1(str(M).encode('utf-8')).hexdigest()

        # Convert the hash to an integer
        sha1_int = int(sha1_hash, 16)

        # Calculate the number of bits needed to represent range_max
        num_bits_range_max = max.bit_length()
        #bageeb el lsb bta3 sha1  let num_bit=3
        #step1 : 1000
        #step2:1000 -1 = 0111
        #step3:ANDing with sha1 int 
        #minus 1 from the bits to ensure it is less than q
        LSB = sha1_int & ((1 << (num_bits_range_max-1)) - 1)
        return LSB
    

    #calculate modulo inverse
    def mod_of_inverse(self, number, modulus):
        # Calculate the inverse of the number modulo modulus
        inverse = pow(number, -1, modulus)
        modulus_of_inverse = inverse % modulus
        return modulus_of_inverse
    
    
    def Verify_signature(self,paramater_list,a,q):
        V=pow(paramater_list[0],paramater_list[1])*pow(paramater_list[1],paramater_list[2])
        m=self.get_m(paramater_list[0],q-1)
        W=pow(a,m)
        if(V==W):
            return True
        else:
            return False


    def Signing_key(self,a,q,Ya,Xa2):
            M=Ya
            m=self.get_m(M,q-1)

            #generate K a random integer
            #Ka = int(random.random()) + random.randint(q, a)
            if a>q:
                Ka = random.randint(q, a)
            else:
                Ka = random.randint(a, q)
            S1a=pow(a,Ka) % q
            Ka_inv=self.mod_of_inverse(Ka,q-1)   
            S2a=Ka_inv*(m-Xa2*S1a)%(q-1)

            #Sending the parameters to BOb
            return S1a,S2a          
    

