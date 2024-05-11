import socket
import threading
import hashlib
import random
#calculate sha1 of a number
def get_m(M,max):
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
def mod_of_inverse(number, modulus):
    # Calculate the inverse of the number modulo modulus
    inverse = pow(number, -1, modulus)
    modulus_of_inverse = inverse % modulus

    return modulus_of_inverse
def Verify_signature(paramater_list,a,q):
    V=pow(paramater_list[0],paramater_list[1])*pow(paramater_list[1],paramater_list[2])
    m=get_m(paramater_list[0],q-1)
    W=pow(a,m)
    if(V==W):
        return True
    else:
        return False
    
def Signing_key(a,q,Ya,Xa2):
        M=Ya
        m=get_m(M,q-1)

        #generate K a random integer
        Ka=random.randint(a,q)
        S1a=pow(a,Ka) % q
        Ka_inv=mod_of_inverse(Ka,q-1)   
        S2a=Ka_inv*(m-Xa2*S1a)%(q-1)

        #Sending the parameters to BOb
        gamal_parameters=[Ya,S1a,S2a]
        return gamal_parameters            


# function to terminate the connection
def stop_connection(connection):
    connection.close()

# Function to handle receiving messages
def receive_messages(connection):
    while True:
        try:
            data = connection.recv(1024)
            message = data.decode()
            print(message)
            if message.strip().lower() == "end":
                print("Connection ended by remote user.")
                stop_connection(connection)
                break
        except ConnectionResetError:
            break


# Function to handle sending messages
def send_message(connection):
    while True:
        message = input()
        connection.send(message.encode())
        if message.strip().lower() == "end":
            print("Connection ended.")
            stop_connection(connection)
            break


# Function to create a server
def create_server(p, g,q,a):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('localhost', 8000))
        server.listen()

        print("First peer started. Waiting for connections...")
        while True:
            connection, address = server.accept()
            print(f"Connected to {address}")
            #Establish ElGamal parameters
            Xa2 = 3
            Ya2 = pow(a,Xa2) % q 
            connection.send(str(Ya2).encode())
            Yb2 = int(connection.recv(1024).decode())
            # stablish the deffie hellman key
            Xa = 4
            Ya = pow(g,Xa) % p 
            #signing Alice public key
            gamal_parameters=Signing_key(a,q,Ya,Xa2)
            # Convert numbers to a string with a delimiter (e.g., comma)
            gamal_parameters_str = ','.join(map(str, gamal_parameters))
            connection.send(gamal_parameters_str.encode())

            # #verifying Bob signature
            # # Receive the string containing the numbers 
            # Bob_gamal = connection.recv(1024).decode()
            # # Split the string into individual numbers
            # Bob_gamal_int = list(map(int, Bob_gamal.split(',')))
            # if(Verify_signature(Bob_gamal_int,a,q)):
            #      stop_connection()


            # ########DEFFIE-HELLMAN######
            # key = pow(Bob_gamal_int[0], Xa) % p
            # print("the key is ", key)          


            threading.Thread(target=receive_messages, args=(connection,)).start()
            threading.Thread(target=send_message, args=(connection,)).start()
    except Exception:
        return -1



# Function to create a client
def create_client(p, g,q,a):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 8000))

    # stablish the elgamal
    Xb2 = 1
    Yb2 = pow(a,Xb2)%q
    client.send(str(Yb2).encode())
    Ya2 = int(client.recv(1024).decode())
  

    # stablish the deffie helman key
    Xb = 3
    Yb = pow(g,Xb)%p
    # client.send(str(Yb).encode())
    # Ya = int(client.recv(1024).decode())
    # key = pow(Ya, Xb) % p
    # print("the key is ", key)

    #verifying alice signature
    # Receive the string containing the numbers
    Alice_gamal = client.recv(1024).decode()

    # # Split the string into individual numbers
    # Alice_gamal_int = list(map(int, Alice_gamal.split(',')))
    # if(Verify_signature(Alice_gamal_int,a,q)):
    #    stop_connection()

    # #signing Alice public key
    # gamal_parameters=Signing_key(a,q,Yb,Xb2)
    # # Convert numbers to a string with a delimiter (e.g., comma)
    # gamal_parameters_str = ','.join(map(str, gamal_parameters))
    # client.send(gamal_parameters_str.encode())

    # ########DEFFIE-HELLMAN######
    # key = pow(Alice_gamal_int[0], Xb) % p
    # print("the key is ", key)    


    threading.Thread(target=receive_messages, args=(client,)).start()
    threading.Thread(target=send_message, args=(client,)).start()


# Function to start either server or client
def start_peer(p, g,q,a):
    if create_server(p, g,q,a) == -1:
        print("creating the other peer of chat...\n")
        create_client(p, g,q,a)
    

