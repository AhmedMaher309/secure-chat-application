import socket
import threading
from hashlib import sha256
from elgamal import Elgamal
from Crypto.Cipher import AES
from base64 import b64encode, b64decode


# function to terminate the connection
def stop_connection(connection):
    connection.close()

# Function to handle receiving messages
def receive_messages(connection, decryptor):
    while True:
        try:
            data = connection.recv(1024)
            message = decryptor.decrypt(data)
            message = message[:-message[-1]]
            message = message.decode()
            print(message)
            if message.strip().lower() == "end":
                print("Connection ended by remote user.")
                stop_connection(connection)
                break
        except ConnectionResetError:
            break


# Function to handle sending messages
def send_message(connection, encryptor):
    while True:
        message = input()
        message_to_send = message.encode()
        padding_length = 16 - (len(message_to_send) % 16)
        message_to_send += bytes([padding_length] * padding_length)
        encrypted_message = encryptor.encrypt(message_to_send)
        connection.send(encrypted_message)
        if message.strip().lower() == "end":
            print("Connection ended.")
            stop_connection(connection)
            break


# Function to create a server
def create_server(p, g, a, q):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('localhost', 9999))
        server.listen()

        print("First peer started. Waiting for connections...")
        while True:
            connection, address = server.accept()
            print(f"Connected to {address}")

            # establish the deffie hellman key
            Xa = 4
            Ya = pow(g,Xa) % p 

            # establish the elgamal key
            Xa2 = 3
            Ya2 = pow(a, Xa2) % q
            connection.send(str(Ya2).encode())
            Yb2 = int(connection.recv(1024).decode())
            S1a, S2a = Elgamal.Signing_key(a,q,Ya,Xa2)

            connection.send(str(S1a).encode())
            S1b = int(connection.recv(1024).decode())
            connection.send(str(S2a).encode())
            S2b = int(connection.recv(1024).decode())

            connection.send(str(Ya).encode())
            Y_other = int(connection.recv(1024).decode())
            verify = Elgamal.Verify_signature(S1b, S2b, Yb2, Y_other, a, q)

            if verify == False:
                print("the key is not verified")
                return -1
            
            key = pow(Y_other, Xa) % p
            key = sha256(str(key).encode()).digest()
            print("the key is ", key)

            encryptor = AES.new(key, AES.MODE_ECB)
            decryptor = AES.new(key, AES.MODE_ECB)


            threading.Thread(target=receive_messages, args=(connection, decryptor)).start()
            threading.Thread(target=send_message, args=(connection, encryptor)).start()
    except Exception:
        return -1



# Function to create a client
def create_client(p, g, a, q):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 9999))


    # establish the deffie helman key
    Xb = 3
    Yb = pow(g,Xb)%p

    # establish the elgamal key
    Xb2 = 5
    Yb2 = pow(a, Xb2) % q
    Ya2 = int(client.recv(1024).decode())
    client.send(str(Yb2).encode())
    S1b, S2b = Elgamal.Signing_key(a,q,Yb,Xb2)

    S1a = int(client.recv(1024).decode())
    client.send(str(S1b).encode())
    S2a = int(client.recv(1024).decode())
    client.send(str(S2b).encode())
 

    Y_other = int(client.recv(1024).decode())
    client.send(str(Yb).encode())
    verify = Elgamal.Verify_signature(S1a, S2a, Ya2, Y_other, a, q)

    if verify == False:
        print("the key is not verified")
        return -1

    key = pow(Y_other, Xb) % p
    key = sha256(str(key).encode()).digest()
    print("the key is ", key)

    encryptor = AES.new(key, AES.MODE_ECB)
    decryptor = AES.new(key, AES.MODE_ECB)



    threading.Thread(target=receive_messages, args=(client, decryptor)).start()
    threading.Thread(target=send_message, args=(client, encryptor)).start()


# Function to start either server or client
def start_peer(p, g, a, q):
    if create_server(p, g, a, q) == -1:
        print("creating the other peer of chat...\n")
        create_client(p, g, a, q)
    

