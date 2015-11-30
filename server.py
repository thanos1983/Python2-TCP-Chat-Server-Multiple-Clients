#!/usr/bin/python
__author__ = 'Athanasios Garyfalos'

# Tcp Chat server
import socket, select, sys

def checkArgumentInput( argumentInputList  ) :

    if len( argumentInputList ) != 2 :
        print 'Usage : python {} [IP:PORT]' .format(argumentInputList[0])
        sys.exit(1)
    elif ":" not in argumentInputList[1] :
        print 'Usage : [IP:PORT] ({})' .format(argumentInputList[1])
        sys.exit(1)
    elif argumentInputList[1].count(':') > 1 :
        print 'Usage : [IP:PORT] ({})' .format(argumentInputList[1])
        sys.exit(1)

    hostnameAndPort = argumentInputList[1].split(":")

    if not hostnameAndPort[0] or \
       not hostnameAndPort[1] :
        print 'Usage : python {} [IP:PORT]' .format(argumentInputList[0])
        sys.exit(1)

    if not hostnameAndPort[1].isdigit() or \
       int(hostnameAndPort[1]) < 0 or \
       int(hostnameAndPort[1]) > 65535 :
        print 'Please enter a valid port number : ({})' .format(hostnameAndPort[1])
        sys.exit(1)

    try :
        socket.inet_aton(hostnameAndPort[0])
    except socket.error :
        print 'Please use a valid IP syntax: {}' .format(hostnameAndPort[0])
        sys.exit(1)

    return (hostnameAndPort[0], int(hostnameAndPort[1]))

def initialization(serverSocket) :

    serverSocket.send('Hello version\n')
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

    return clientNickname

#Function to broadcast chat messages to all connected clients
def broadcast_data (sock, message) :
    #Do not send the message to master socket and the client who has send us the message
    for socket in CONNECTION_LIST :
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection may be, chat client pressed ctrl+c for example
                socket.close()
                CONNECTION_LIST.remove(socket)

if __name__ == "__main__" :

    BUFFER_RCV = 512
    MAX_BUFFER_RCV = 255

    host, port = checkArgumentInput( sys.argv )

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this has no effect, why ?
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(10)

    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)

    print "Chat server started on port " + str(port)

    # Initialization to bind the port with the name
    dictionary = {}

    while 1 :
        # Get the list sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select( CONNECTION_LIST,
                                                                  [],
                                                                  [] )

        for sock in read_sockets :
            #New connection
            if sock == server_socket :
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                newUserNickname = initialization(sockfd)
                dictionary[addr[1]] = newUserNickname
                print "Client (%s, %s) connected" % addr

                broadcast_data(sockfd, "[%s:%s] entered room\n" % addr)

            #Some incoming message from a client
            else :
                # Data recieved from client, process it
                try :
                    #In Windows, sometimes when a TCP program closes abruptly,
                    # a "Connection reset by peer" exception will be thrown
                    data = sock.recv(BUFFER_RCV)
                    data = data.rstrip('\r\n')
                    broadcastingHost, broadcastingSocket = sock.getpeername()
                    if len(data) > MAX_BUFFER_RCV :
                        sock.send('ERROR please send less than 256 characters!\n')
                    elif 'MSG' not in data :
                        sock.send('ERROR the received text is not correctly fomatted e.g. "MSG nick txt"\n')
                        # Clossing binded port client with server due to ERROR
                        # Removing socket from list in future broadcast
                        sock.close()
                        CONNECTION_LIST.remove(sock)
                        del dictionary[broadcastingSocket]
                    elif 'exit' in data or \
                         'quit' in data :
                        # Clossing binded port client with server due to client
                        # request. Removing socket from list in future broadcast
                        sock.close()
                        CONNECTION_LIST.remove(sock)
                        del dictionary[broadcastingSocket]
                    else :
                        tmp = []
                        tmp = data.split(' ', 1)
                        data = tmp[1]
                        data + '\n'
                        broadcast_data(sock, "\r" + "<" + tmp[0] + " " + dictionary[broadcastingSocket] + "> " + data)
                except :
                    broadcast_data(sock, "Client (%s, %s) is offline" % addr)
                    print "Client (%s, %s) is offline" % addr
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue

    server_socket.close()
    sys.exit(0)
