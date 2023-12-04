import socket

def client_program():
    host = socket.gethostname()
    port = 8000

    client_socket = socket.socket()
    client_socket.connect((host,port))

    while(True):
        #message = "tell me about Thai-nichi institute of technology"
        message = input("user's question : ")
        if (message == 'exit'):
            client_socket.close()    
        client_socket.send(message.encode())
                    


client_program()