#!/usr/bin/python
import socket
import select
import sys

__author__ = 'Athanasios Garyfalos'

# Tcp Chat server


def check_argument_input(argument_input_list):

    if len(argument_input_list) != 2:
        print 'Usage : python {} [IP:PORT]' .format(argument_input_list[0])
        sys.exit(1)
    elif ":" not in argument_input_list[1]:
        print 'Usage : [IP:PORT] ({})' .format(argument_input_list[1])
        sys.exit(1)
    elif argument_input_list[1].count(':') > 1:
        print 'Usage : [IP:PORT] ({})' .format(argument_input_list[1])
        sys.exit(1)

    host_name_and_port = argument_input_list[1].split(":")

    if not host_name_and_port[0] or \
            not host_name_and_port[1]:
        print 'Usage : python {} [IP:PORT]' .format(argument_input_list[0])
        sys.exit(1)

    if not host_name_and_port[1].isdigit() or \
        int(host_name_and_port[1]) < 0 or \
            int(host_name_and_port[1]) > 65535:
        print 'Please enter a valid port number : ({})' .format(host_name_and_port[1])
        sys.exit(1)

    try:
        socket.inet_aton(host_name_and_port[0])
    except socket.error:
        print 'Please use a valid IP syntax: {}' .format(host_name_and_port[0])
        sys.exit(1)

    return host_name_and_port[0], int(host_name_and_port[1])


def initialization(transmitting_socket):

    transmitting_socket.send('Hello version\n')
    data_to_send = transmitting_socket.recv(512)
    data_to_send = data_to_send.rstrip('\r\n')

    if 'NICK' not in data_to_send:
        transmitting_socket.send('ERROR : NICK was not included please check again\n')
        return
    else:
        nickname_prefix, client_nickname = data_to_send.split(' ', 1)
        if not (client_nickname.isalnum()):
            transmitting_socket.send('ERROR : username contains special characters\n')
            return
        elif len(client_nickname) > 12:
            transmitting_socket.send('ERROR : username longer than 12 characters\n')
            return
        else:
            transmitting_socket.send('OK\n')

    return client_nickname


# Function to broadcast chat messages to all connected clients
def broadcast_data(transmitting_sock, message):
    # Do not send the message to master socket and the client who has send us the message
    for know_socket in CONNECTION_LIST:
        if know_socket != server_socket and know_socket != transmitting_sock:
            know_socket.send(message)

if __name__ == "__main__":

    BUFFER_RCV = 512
    MAX_BUFFER_RCV = 255

    host, port = check_argument_input(sys.argv)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this has no effect, why ?
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(10)

    # List to keep track of socket descriptors
    CONNECTION_LIST = list([])
    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)

    print "Chat server started on port " + str(port)

    # Initialization to bind the port with the name
    dictionary = {}

    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST,
                                                                   [],
                                                                   [])

        for sock in read_sockets:
            # New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection received through server_socket
                socket_fd, address = server_socket.accept()
                CONNECTION_LIST.append(socket_fd)
                newUserNickname = initialization(socket_fd)
                dictionary[address[1]] = newUserNickname
                print "Client ({}, {}) connected" .format(address[0], address[1])
            # Some incoming message from a client
            else:
                # Data received from client, process it
                data = sock.recv(BUFFER_RCV)
                data = data.rstrip('\r\n')
                broadcastingHost, broadcastingSocket = sock.getpeername()
                if len(data) > MAX_BUFFER_RCV:
                    sock.send('ERROR please send less than 256 characters!\n')
                elif 'MSG' not in data:
                    sock.send('ERROR the received text is not correctly formatted e.g. "MSG nick txt"\n')
                    # Closing bind port client with server due to ERROR
                    # Removing socket from list in future broadcast
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    del dictionary[broadcastingSocket]
                elif 'exit' in data or \
                        'quit' in data:
                    # Closing bind port client with server due to client
                    # request. Removing socket from list in future broadcast
                    broadcast_data(sock,
                                   "\r" + "<Client " +
                                   dictionary[broadcastingSocket] + " has left the room>\n")
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    del dictionary[broadcastingSocket]
                else:
                    tmp = []
                    tmp = data.split(' ', 1)
                    data = tmp[1]
                    broadcast_data(sock,
                                   "\r" + "<" + tmp[0] + " " + dictionary[broadcastingSocket] + "> " + data + "\n")

    server_socket.close()
    sys.exit(0)
