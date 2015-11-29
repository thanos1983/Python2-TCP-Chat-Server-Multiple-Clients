#!/usr/bin/python
__author__ = 'Athanasios Garyfalos'

# telnet program example
import re
import socket, select, string, sys
BUFFER_RCV = 256

def checkArgumentInput( argumentInputList  ):

    if len( argumentInputList ) != 3 :
        print 'Usage : python {} [IP:PORT] [NickName]' .format(argumentInputList[0])
        sys.exit(1)
    elif ":" not in argumentInputList[1] :
        print 'Usage : [IP:PORT] [NickName] ({})' .format(argumentInputList[1])
        sys.exit(1)
    elif argumentInputList[1].count(':') > 1 :
        print 'Usage : [IP:PORT] [NickName] ({})' .format(argumentInputList[1])
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

    try:
        socket.inet_aton(hostnameAndPort[0])
    except socket.error:
        print 'Please use a valid IP syntax: {}' .format(hostnameAndPort[0])
        sys.exit(1)

    return (hostnameAndPort[0], int(hostnameAndPort[1]), argumentInputList[2])

def initialization( clientSocket, userNickname ) :

    data = clientSocket.recv(BUFFER_RCV)
    data = data.rstrip('\r\n')

    if 'Hello version' not in data :
        print 'User connection is terminated, Server is not configured for this client!\n'
        clientSocket.close()
        sys.exit(1)
    else :
        clientSocket.send('NICK ' + userNickname)
        data = ''
        data = clientSocket.recv(BUFFER_RCV)
        data = data.rstrip('\r\n')

        if 'ERROR' in data :
            print data
            clientSocket.close()
            sys.exit(1)
        else :
            return

def prompt() :
    sys.stdout.write('<You> ')
    sys.stdout.flush()

#main function
if __name__ == "__main__":

    host, port, nickName = checkArgumentInput( sys.argv )

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)

    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit(1)

    initialization(s, nickName)
    print 'Connected to remote host. Start sending messages'
    prompt()

    while 1:
        socket_list = [sys.stdin, s]

        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select( socket_list,
                                                                    [],
                                                                    [] )

        for sock in read_sockets:
            #incoming message from remote server
            if sock == s:
                data = sock.recv(BUFFER_RCV)
                data = data.rstrip('\r\n')
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                elif 'ERROR' in data:
                    print data
                    sys.exit(1)
                else :
                    print data
                    #sys.stdout.write(data)
                    prompt()

            #user entered a message
            else :
                msg = sys.stdin.readline()
                if msg.isspace() :
                    print 'Please enter a string not empty.'
                    prompt()
                elif 'exit' in msg or \
                     'quit' in msg :
                    print 'Client requested to shutdown, GoodBye!'
                    msg = 'MSG ' + msg
                    s.send(msg)
                    s.close()
                    sys.exit(0)
                else :
                    msg = 'MSG ' + msg
                    s.send(msg)
                    prompt()
