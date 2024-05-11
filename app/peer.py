import socket
import threading
from elgamal import Elgamal

gamal = Elgamal()
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
def create_server(p, g, a, q):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('localhost', 9999))
        server.listen()

        print("First peer started. Waiting for connections...")
        while True:
            connection, address = server.accept()
            print(f"Connected to {address}")


            # establish el gamal signature 
            Xa2 = 3
            Ya2 = pow(a,Xa2) % q 
            connection.send(str(Ya2).encode())
            Yb2 = int(connection.recv(1024).decode())
            print("the key is yb2 ", Yb2)
            # establish the deffie hellman key
            Xa = 4
            Ya = pow(g,Xa) % p 

            #signing Alice public key
            S1a, S2a = gamal.Signing_key(a,q,Ya,Xa2)
            # Convert numbers to a string with a delimiter (e.g., comma)
            gamal_parameters_str = ','.join(map(str, [S1a, S2a]))
            print(gamal_parameters_str)
            connection.send(gamal_parameters_str.encode())

            connection.send(str(Ya).encode())
            Y_other = int(connection.recv(1024).decode())
            key = pow(Y_other, Xa) % p
            print("the key is ", key)


            threading.Thread(target=receive_messages, args=(connection,)).start()
            threading.Thread(target=send_message, args=(connection,)).start()
    except Exception:
        return -1



# Function to create a client
def create_client(p, g, a, q):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 9999))

    # establish el gamal signature
    Xb2 = 1
    Yb2 = pow(a,Xb2)%q
    client.send(str(Yb2).encode())
    Ya2 = int(client.recv(1024).decode())
    print("the key is ya2   ", Ya2)

    # stablish the deffie helman key
    Xb = 3
    Yb = pow(g,Xb)%p

    #verifying alice signature

    # Receive the string containing the numbers
    Alice_gamal = client.recv(1024).decode()
    #print(Alice_gamal)
    Alice_gamal_list = Alice_gamal.split(',')
    Alice_gamal_cleaned_list = [x for x in Alice_gamal_list if x != '']
    # # Convert each element to an integer
    Alice_gamal_integers = [int(x) for x in Alice_gamal_cleaned_list if x.strip()]
    print(Alice_gamal_integers)




    # establish the deffie helman key
    client.send(str(Yb).encode())
    Y_other = int(client.recv(1024).decode())
    key = pow(Y_other, Xb) % p
    print("the key is ", key)


    threading.Thread(target=receive_messages, args=(client,)).start()
    threading.Thread(target=send_message, args=(client,)).start()


# Function to start either server or client
def start_peer(p, g, a, q):
    if create_server(p, g, a, q) == -1:
        print("creating the other peer of chat...\n")
        create_client(p, g, a, q)
    

