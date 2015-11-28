#!/usr/bin/python
__author__ = 'Athanasios Garyfalos'

# TCP Chat Server

import sys  #for exit
import socket, select

def initialization(serverSocket) :

    data = 'Hello version\n'
    serverSocket.send(data)
    data = serverSocket.recv(512)
    data = data.rstrip('\r\n')

    if 'NICK' not in data :
        serverSocket.send('ERROR : NICK was not included please check again\n')
        return
    else :
        (NICK, clientNickname) = data.split(' ', 1 )
        if not (clientNickname.isalnum()) :
            serverSocket.send('ERROR : username contains special characters\n')
            return
        elif (len(clientNickname) > 12) :
            serverSocket.send('ERROR : username longer than 12 characters\n')
            return
        else :
            serverSocket.send('OK\n')
            data = ''
            data = serverSocket.recv(512)
            data = data.rstrip('\r\n')

            if 'MSG' not in data :
                serverSocket.send('ERROR : MSG was not included please check again\n')
                return
            else :
                return clientNickname

#Function to broadcast chat messages to all connected clients
def broadcast_data (sock, message):
    #Do not send the message to master socket and the client who has send us the message
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection may be, chat client pressed ctrl+c for example
                socket.close()
                CONNECTION_LIST.remove(socket)

if __name__ == "__main__":

    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
    PORT = 5000

    #create an AF_INET, STREAM socket (TCP)
    try:
        server_socket = socket.socket( socket.AF_INET,
                                       socket.SOCK_STREAM )
    except socket.error, msg:
        print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
        sys.exit();

    # this has no effect, why ?
    server_socket.setsockopt( socket.SOL_SOCKET,
                              socket.SO_REUSEADDR,
                              1 )
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10) # Backlog connections in queue

    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)

    print "Chat server started on port " + str(PORT)
    dictionary = {}

    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])

        for sock in read_sockets:
            #New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)

                newUserNickname = initialization(sockfd)

                if newUserNickname is not None :
                    dictionary[addr[1]] = newUserNickname
                    print dictionary
                    print "Client (%s, %s) connected" % addr
                    broadcast_data(sockfd, "[{}] entered room\n" .format(newUserNickname))
                else :
                    CONNECTION_LIST.remove(sockfd)

            #Some incoming message from a client
            else:
                # Data recieved from client, process it
                try:
                    #In Windows, sometimes when a TCP program closes abruptly,
                    # a "Connection reset by peer" exception will be thrown
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        broadcast_data(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data)                

                except:
                    broadcast_data(sock, "Client (%s, %s) is offline" % addr)
                    print "Client (%s, %s) is offline" % addr
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue

    server_socket.close()
