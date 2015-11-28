#!/usr/bin/python
__author__ = 'Athanasios Garyfalos'

# TCP chat Client
import socket, select, sys

def prompt(userNickname) :
    sys.stdout.write(userNickname + ': ')
    sys.stdout.flush()
    return

def initialization( clientSocket, userNickname ) :

    data = clientSocket.recv(256)
    data = data.rstrip('\r\n')

    if 'Hello version' not in data :
        print 'User connection is terminated, Server is not configured for this client!\n'
        clientSocket.shutdown(SHUT_RDWR)
        clientSocket.close()
        sys.exit()
    else :
        clientSocket.send('NICK ' + userNickname)

        data = ''
        data = clientSocket.recv(256)
        data = data.rstrip('\r\n')

        if 'ERROR' in data :
            print data
            clientSocket.shutdown(SHUT_RDWR)
            clientSocket.close()
            sys.exit()
        else :
            return

def checkArgumentInput( argumentInputList  ):

    if len( argumentInputList ) != 3 :
        print 'Usage : python {} hostname:port nickname' .format(argumentInputList[0])
        sys.exit(1)
    elif ":" not in argumentInputList[1] :
        print 'Usage : hostname:port ({}) nickname' .format(argumentInputList[1])
        sys.exit(1)
    elif argumentInputList[1].count(':') > 1 :
        print 'Usage : hostname:port ({}) nickname' .format(argumentInputList[1])
        sys.exit(1)

    hostnameAndPort = argumentInputList[1].split(":")

    if not hostnameAndPort[0] or \
       not hostnameAndPort[1] :
        print 'Usage : python {} hostname:port' .format(argumentInputList[0])
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

#main function
if __name__ == "__main__":

    host, port, nickName = checkArgumentInput( sys.argv )

    #create an INET, STREAMing socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
    except socket.error:
        print 'Failed to create socket'
        sys.exit()

    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()

    print 'Connected to remote host. Start sending messages'
    initialization(s, nickName)
    prompt(nickName)

    while 1:
        socket_list = [sys.stdin, s]

        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select( socket_list ,
                                                                    [] ,
                                                                    [] )

        for sock in read_sockets:
            #incoming message from remote server
            if sock == s:
                data = ''
                data = sock.recv(256)
                if 'ERROR' in data :
                    print data
                    sock.shutdown(SHUT_RDWR)
                    sock.close()
                    sys.exit()
                else :
                    data = data.rstrip('\r\n')
                    print
                    print data
                    prompt(nickName)

            #user entered a message
            else :
                msg = sys.stdin.readline()
                msg = 'MSG ' + msg
                s.send(msg)
                #prompt(nickName)
