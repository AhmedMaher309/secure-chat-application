import socket
import threading

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
def create_server(p, g):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('localhost', 9999))
        server.listen()

        print("First peer started. Waiting for connections...")
        while True:
            connection, address = server.accept()
            print(f"Connected to {address}")

            # stablish the deffie hellman key
            x = 4
            y = pow(g,x) % p 
            connection.send(str(y).encode())
            y_other = int(connection.recv(1024).decode())
            key = pow(y_other, x) % p
            print("the key is ", key)


            threading.Thread(target=receive_messages, args=(connection,)).start()
            threading.Thread(target=send_message, args=(connection,)).start()
    except Exception:
        return -1



# Function to create a client
def create_client(p, g):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 9999))

    # stablish the deffie helman key
    x = 3
    y = pow(g,x)%p
    client.send(str(y).encode())
    y_other = int(client.recv(1024).decode())
    key = pow(y_other, x) % p
    print("the key is ", key)


    threading.Thread(target=receive_messages, args=(client,)).start()
    threading.Thread(target=send_message, args=(client,)).start()


# Function to start either server or client
def start_peer(p, g):
    if create_server(p, g) == -1:
        print("creating the other peer of chat...\n")
        create_client(p, g)
    

