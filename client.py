#!/usr/bin/python
import select
import socket
import sys

__author__ = 'Athanasios Garyfalos'

# telnet program example
BUFFER_RCV = 256


def check_argument_input(argument_input_list):
    if len(argument_input_list) != 3:
        sys.stdout.write('Usage : python {} [IP:PORT] [NickName]\n'.format(argument_input_list[0]))
        sys.stdout.flush()
        sys.exit(1)
    elif ":" not in argument_input_list[1]:
        sys.stdout.write('Usage : python {} [IP:PORT] please a column\n'.format(argument_input_list[0]))
        sys.stdout.flush()
        sys.exit(1)
    elif argument_input_list[1].count(':') > 1:
        sys.stdout.write('Usage : python {} [IP:PORT] please one column\n'.format(argument_input_list[0]))
        sys.stdout.flush()
        sys.exit(1)

    hostname_and_port = argument_input_list[1].split(":")

    if not hostname_and_port[0] or \
            not hostname_and_port[1]:
        sys.stdout.write('Usage : python {} [IP:PORT]\n'.format(argument_input_list[0]))
        sys.stdout.flush()
        sys.exit(1)

    if not hostname_and_port[1].isdigit() or \
            int(hostname_and_port[1]) < 0 or \
            int(hostname_and_port[1]) > 65535:
        sys.stdout.write('Please use a valid port number "0 - 65535"\n'.format(argument_input_list[1]))
        sys.stdout.flush()
        sys.exit(1)

    try:
        socket.inet_aton(hostname_and_port[0])
    except socket.error:
        sys.stdout.write('Please use a valid IP syntax: {}'.format(hostname_and_port[0]))
        sys.stdout.flush()
        sys.exit(1)

    return hostname_and_port[0], int(hostname_and_port[1]), argument_input_list[2]


def initialization(client_socket, user_nickname):
    rcv_data = client_socket.recv(BUFFER_RCV)
    rcv_data = rcv_data.rstrip('\r\n')

    if 'Hello version' not in rcv_data:
        sys.stdout.write('User connection is terminated, Server is not configured for this client!\n')
        sys.stdout.flush()
        client_socket.close()
        sys.exit(1)
    else:
        client_socket.send('NICK ' + user_nickname)
        rcv_data = client_socket.recv(BUFFER_RCV)
        rcv_data = rcv_data.rstrip('\r\n')

        if 'ERROR' in rcv_data:
            sys.stdout.write(rcv_data + '\n')
            sys.stdout.flush()
            client_socket.close()
            sys.exit(1)
        else:
            return


def prompt():
    sys.stdout.write('<You> ')
    sys.stdout.flush()


# main function
if __name__ == "__main__":

    host, port, nickName = check_argument_input(sys.argv)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)

    # connect to remote host
    # noinspection PyBroadException
    try:
        s.connect((host, port))
    except:
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
        read_sockets, write_sockets, error_sockets = select.select(socket_list,
                                                                   [],
                                                                   [])

        for sock in read_sockets:
            # incoming message from remote server
            if sock == s:
                data = sock.recv(BUFFER_RCV)
                data = data.rstrip('\r\n')
                if not data:
                    sys.stdout.write('\nDisconnected from chat server\n')
                    sys.stdout.flush()
                    sys.exit()
                elif 'ERROR' in data:
                    sys.stdout.write(data)
                    sys.stdout.flush()
                    sys.exit(1)
                else:
                    sys.stdout.write(data + '\n')
                    sys.stdout.flush()
                    prompt()

            # user entered a message
            else:
                msg = sys.stdin.readline()
                msg = msg.rstrip('\r\n')
                if msg.isspace():
                    sys.stdout.write('Please enter a string not empty.\n')
                    sys.stdout.flush()
                    prompt()
                elif 'exit' in msg or \
                        'quit' in msg:
                    sys.stdout.write('Client requested to shutdown, GoodBye!\n')
                    sys.stdout.flush()
                    msg = 'MSG ' + msg
                    s.send(msg)
                    s.close()
                    sys.exit(0)
                else:
                    msg = 'MSG ' + msg + '\n'
                    s.send(msg)
                    prompt()
