#!/usr/bin/python
__author__ = 'Athanasios Garyfalos'

import argparse
import sys

def checkArgumentInput( argumentInputList  ):
    parser = argparse.ArgumentParser( prog        = argumentInputList[0],
                                      usage       = '%(prog)s [input file]',
                                      description = 'Process ASCII File',
                                      epilog      = 'Display the contents of a given ASCII file.' )
    parser.add_argument( 'inFileName',
                         type  = argparse.FileType('r'),
                         help  = "'Source' ASCII file to be processed." )
    args = parser.parse_args()

    if '.txt' not in str(argumentInputList[1]):
        print '\nPlease use a source file with the ".txt" extension: %s\n' % str(sys.argv[1])
        sys.exit(1)
        return

def processInputAsciiFile( asciiFile ):
    non_blank_lines = chars = 0
    with open(asciiFile, 'r') as fr:
        for line in fr:
            chars += len(line)
            non_blank_lines += 1
            line = line.rstrip('\r\n')
            print line

    fr.closed
    print 'The number of lines: "{}" and number of characters: "{}"'.format(non_blank_lines,chars)
    return '\nCaution: the total number of characters includes the "\\n" new line character\n' 

def main():
    checkArgumentInput( sys.argv )
    print(processInputAsciiFile( sys.argv[1] ))

#main function
if __name__ == "__main__":
main()
sys.exit(0)
