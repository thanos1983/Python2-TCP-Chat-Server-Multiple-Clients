#!/usr/bin/python
__author__ = 'Athanasios Garyfalos'

# telnet program example
import re
import socket, select, string, sys
BUFFER_RCV = 256

def checkArgumentInput( argumentInputList  ):

    if len( argumentInputList ) != 3 :
        sys.stdout.write('Usage : python {} [IP:PORT] [NickName]\n' .format(argumentInputList[0]))
        sys.stdout.flush()
        sys.exit(1)
    elif ":" not in argumentInputList[1] :
        sys.stdout.write('Usage : python {} [IP:PORT] please a column\n' .format(argumentInputList[0]))
        sys.stdout.flush()
        sys.exit(1)
    elif argumentInputList[1].count(':') > 1 :
        sys.stdout.write('Usage : python {} [IP:PORT] please one column\n' .format(argumentInputList[0]))
        sys.stdout.flush()
        sys.exit(1)

    hostnameAndPort = argumentInputList[1].split(":")

    if not hostnameAndPort[0] or \
       not hostnameAndPort[1] :
        sys.stdout.write('Usage : python {} [IP:PORT]\n' .format(argumentInputList[0]))
        sys.stdout.flush()
        sys.exit(1)

    if not hostnameAndPort[1].isdigit() or \
       int(hostnameAndPort[1]) < 0 or \
       int(hostnameAndPort[1]) > 65535 :
        sys.stdout.write('Please use a valid port number "0 - 65535"\n' .format(argumentInputList[1]))
        sys.stdout.flush()
        sys.exit(1)

    try:
        socket.inet_aton(hostnameAndPort[0])
    except socket.error:
        sys.stdout.write('Please use a valid IP syntax: {}' .format(hostnameAndPort[0]))
        sys.stdout.flush()
        sys.exit(1)

    return (hostnameAndPort[0], int(hostnameAndPort[1]), argumentInputList[2])

def initialization( clientSocket, userNickname ) :

    data = clientSocket.recv(BUFFER_RCV)
    data = data.rstrip('\r\n')

    if 'Hello version' not in data :
        sys.stdout.write('User connection is terminated, Server is not configured for this client!\n')
        sys.stdout.flush()
        clientSocket.close()
        sys.exit(1)
    else :
        clientSocket.send('NICK ' + userNickname)
        data = ''
        data = clientSocket.recv(BUFFER_RCV)
        data = data.rstrip('\r\n')

        if 'ERROR' in data :
            sys.stdout.write(data + '\n')
            sys.stdout.flush()
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
        sys.stdout.write('Unable to connect\n')
        sys.stdout.flush()
        sys.exit(1)

    initialization(s, nickName)
    sys.stdout.write('Connected to remote host. Start sending messages\n')
    sys.stdout.flush()
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
                    sys.stdout.write('\nDisconnected from chat server\n')
                    sys.stdout.flush()
                    sys.exit()
                elif 'ERROR' in data:
                    sys.stdout.write(data)
                    sys.stdout.flush()
                    sys.exit(1)
                else :
                    sys.stdout.write(data + '\n')
                    sys.stdout.flush()
                    prompt()

            #user entered a message
            else :
                msg = sys.stdin.readline()
                msg = msg.rstrip('\r\n')
                if msg.isspace() :
                    sys.stdout.write('Please enter a string not empty.\n')
                    sys.stdout.flush()
                    prompt()
                elif 'exit' in msg or \
                     'quit' in msg :
                    sys.stdout.write('Client requested to shutdown, GoodBye!\n')
                    sys.stdout.flush()
                    msg = 'MSG ' + msg
                    s.send(msg)
                    s.close()
                    sys.exit(0)
                else :
                    msg = 'MSG ' + msg + '\n'
                    s.send(msg)
                    prompt()
