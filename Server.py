# Python program to implement server side of chat room.
import socket
import json
from _thread import *


class Server:

    def __init__(self, chief, port):
        self.data = None
        self.chief = chief
        self.port = port

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.list_of_clients = []

    def start_server(self):
        self.server.bind(("localhost", self.port))
        self.server.listen(100)

        print("Client chat started on " + str(self.port))

        while True:
            """Accepts a connection request and stores two parameters, 
            conn which is a socket object for that user, and addr 
            which contains the IP address of the client that just 
            connected"""
            conn, addr = self.server.accept()

            """Maintains a list of clients for ease of broadcasting 
            a message to all available people in the chatroom"""
            self.list_of_clients.append(conn)

            # prints the address of the user that just connected
            print(addr[0] + " connected")

            # creates and individual thread for every user
            # that connects
            start_new_thread(self.client_thread, (conn, addr))

        conn.close()
        self.server.close()

    def client_thread(self, conn, addr):
        while True:
                try:
                    message = conn.recv(2048)
                    if message:
                        self.data = json.loads(message)
                        start_new_thread(self.chief.json_to_data, (self.data, conn))
                        # message_to_send = str.encode("GA started")
                        # conn.send(message_to_send)

                    else:
                        """message may have no content if the connection 
                        is broken, in this case we remove the connection"""
                        self.remove(conn)

                except Exception as ex:
                    print(ex)
                    continue

    """The following function simply removes the object 
    from the list that was created at the beginning of 
    the program"""
    def remove(self, connection):
        if connection in self.list_of_clients:
            self.list_of_clients.remove(connection)
