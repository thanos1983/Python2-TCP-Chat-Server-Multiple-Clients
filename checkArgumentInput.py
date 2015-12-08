#!/usr/bin/python

__author__ = 'Athanasios Garyfalos'


class ArgumentLookupError(LookupError):
    """Exception raised for errors in the input.

    Attributes:

    """
    pass

    def __init__(self, *args):
        self.output = None
        self.argument_list = args

    def validate_argument_input(self, argument_input_list):
        if len(argument_input_list) != 3:
            raise ValueError('Usage : python {} [IP:PORT] [NickName]' .format(argument_input_list[0]))
        else:
            self.output = "Success"
            return self.output

        """elif ":" not in self.argument_input_list[1]:
            self.argument_input_list = \
                'Usage : python {} [IP:PORT] please a column\n'.format(self.argument_input_list[0])
            return self.argument_input_list
        # sys.stdout.flush()
        # sys.exit(1)
        elif self.argument_input_list[1].count(':') > 1:
            self.argument_input_list = \
                'Usage : python {} [IP:PORT] please one column\n'.format(self.argument_input_list[0])
            return self.argument_input_list
        # sys.stdout.flush()
        # sys.exit(1)

        hostname_and_port = self.argument_input_list[1].split(":")

        if not hostname_and_port[0] or \
                not hostname_and_port[1]:
            self.argument_input_list = \
                'Usage : python {} [IP:PORT]\n'.format(self.argument_input_list[0])
            return self.argument_input_list
        # sys.stdout.flush()
        # sys.exit(1)

        if not hostname_and_port[1].isdigit() or \
            int(hostname_and_port[1]) < 0 or \
                int(hostname_and_port[1]) > 65535:
            self.argument_input_list = \
                'Please use a valid port number "0 - 65535"\n'.format(self.argument_input_list[1])
            return self.argument_input_list
        # sys.stdout.flush()
        # sys.exit(1)

        try:
            socket.inet_aton(hostname_and_port[0])
        except socket.error:
            return 'Please use a valid IP syntax: {}'.format(hostname_and_port[0])
        # sys.stdout.flush()
        # sys.exit(1)

        return hostname_and_port[0], int(hostname_and_port[1]), self.argument_input_list[2]"""
