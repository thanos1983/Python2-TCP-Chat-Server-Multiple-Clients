#!/usr/bin/python
__author__ = 'Athanasios Garyfalos'

import re
import sys
import argparse

def checkArgumentInput( argumentInputList  ):

    parser = argparse.ArgumentParser( prog        = argumentInputList[0],
                                      usage       = '%(prog)s [input file] [pattern] [output file]',
                                      description = 'Process ASCII File',
                                      epilog      = 'Process the contents of a given ASCII file.' )
    parser.add_argument( 'inFileName',
                         type  = argparse.FileType('r'),
                         help  = "'Source' ASCII file to be processed." )
    parser.add_argument( 'stringToCompare',
                         help  = "'Pattern' ASCII characters to compare." )
    parser.add_argument( 'outFileName',
                         type  = argparse.FileType('w'),
                         help  = "'Destination' ASCII file to wright the output." )
    args = parser.parse_args()

    if '.txt' not in str(argumentInputList[1]):
        print '\nPlease use a source file with the ".txt" extension: %s\n' % str(sys.argv[1])
        sys.exit(1)
    elif '.txt' not in str(argumentInputList[3]):
        print '\nPlease use a destination file with the ".txt" extension: %s\n' % str(sys.argv[3])
        sys.exit(1)
        return

def processInputAsciiFileWriteToOutputFile( asciiSourceFile, asciiDestinationFile ):
    listOfLines = []
    with open(asciiSourceFile, 'r') as fr:
        with open(asciiDestinationFile, 'w') as fw:
            for line in fr:
                if re.search(sys.argv[2], line):
                    fw.write(line)
                    listOfLines.append(line)
                    line = line.rstrip('\r\n')
                    print line
        fw.closed
    fr.closed
    return listOfLines

def main():
    checkArgumentInput( sys.argv )
    print(processInputAsciiFileWriteToOutputFile( sys.argv[1], sys.argv[3] ))

#main function
if __name__ == "__main__":
main()
sys.exit(0)
