#!/usr/bin/python

import socket

__author__ = 'Athanasios Garyfalos'


class ArgumentLookupError(LookupError):
    """Exception raised for errors in the input.

    Attributes:

    """
    pass

    def __init__(self):
        self.output = None
        self.argument_list = []

    def validate_argument_input(self, argv_list):

        if len(argv_list) != 3:
            raise ValueError('Usage1 : python {} [IP:PORT] [NickName]'
                             .format(argv_list[0]))
        elif ":" not in argv_list[1]:
            raise ValueError('Usage2 : python {} [IP:PORT] [NickName]'
                             .format(argv_list[0]))
        elif argv_list[1].count(':') > 1:
            raise ValueError('Usage3 : python {} [IP:PORT] please one column'
                             .format(argv_list[0]))

        hostname_and_port = argv_list[1].split(":")

        if not hostname_and_port[0] or \
           not hostname_and_port[1]:
            raise ValueError('Usage4 : python {} [IP:PORT] insert data'
                             .format(argv_list[0]))

        if not hostname_and_port[1].isdigit() or \
           int(hostname_and_port[1]) < 0 or \
           int(hostname_and_port[1]) > 65535:
            raise ValueError('Please use a valid port number "0 - 65535"'
                             .format(argv_list[1]))

        try:
            socket.inet_aton(hostname_and_port[0])
        except socket.error:
            raise ValueError('Please use a valid IP syntax: {}'
                             .format(hostname_and_port[0]))

        if hostname_and_port[0].count('.') != 3:
            raise ValueError('Please use a valid IP syntax: {}'
                             .format(hostname_and_port[0]))

        self.argument_list.insert(0, hostname_and_port[0])
        self.argument_list.insert(1, int(hostname_and_port[1]))
        self.argument_list.insert(2, argv_list[2])

        return self.argument_list
