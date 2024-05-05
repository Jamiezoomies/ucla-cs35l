#!/usr/bin/python3

import argparse, random, re, select, sys

class shuf:
    # read stdin
    def readStdin(self, stdin):
        self.lines = stdin
    
    # read a file
    def readFile(self, filename):
        f = open(filename, 'r')
        self.lines = f.readlines()
        f.close()

    # output values from LO to HI
    def range(self, value):
        if not re.match(r'^[0-9]+\-[0-9]+$', value):
            raise ValueError("invalid input range")
        start, end = [int(x) for x in value.split('-')]
        if (start > end):
            raise ValueError("invalid input range")
        self.lines = [str(i) for i in range(start, end+1)]
        random.shuffle(self.lines)
        self.appendNewLine()

    # output at most count lines
    def head(self, end):
        self.lines = (self.lines[0:end])

    # shuffle lines
    def shuffle(self):
        random.shuffle(self.lines)

    # get inputs as lines and output shuffled lines
    def echo(self, lines):
        self.lines = lines
        random.shuffle(self.lines)
        self.appendNewLine()

    # append new line for each line
    def appendNewLine(self):
        self.lines = [line + '\n' for line in self.lines]

    # display all lines one time
    def display(self):
        if hasattr(self, 'lines') and self.lines:
            sys.stdout.writelines(self.lines)

    # display all lines repeatedly
    def repeat(self):
        while True:
            self.display()

def main():
    parser = argparse.ArgumentParser(
            description="Write a random permutation of the input lines to standard output.")

    parser.add_argument('filename', nargs='?', default=None, help='Input file name')
    parser.add_argument('-e', '--echo', nargs='*', help='treat each ARG as an input line' )
    parser.add_argument('-i', '--input-range', nargs='?', help='treat each number LO through HI as an input line')
    parser.add_argument('-n', '--head-count', nargs='?', type=int, help='output at most COUNT lines')
    parser.add_argument('-r', '--repeat', action='store_true', help='output lines can be repeated')
    
    args = parser.parse_args()
    
    try:
        # validate the combined option
        if args.input_range and args.echo:
            raise ValueError("Error: cannot use --input-range and --echo together.")

        generator = shuf()
        # echo
        if args.echo is not None:
            generator.echo(args.echo)
        # input range
        elif args.input_range is not None:
            generator.range(args.input_range)
        # if a stdin exists, read the std input and shuffle lines
        elif select.select([sys.stdin], [], [], 0.0)[0]:
            generator.readStdin(sys.stdin.readlines())
            generator.shuffle()
        # if a filename exists, read the file and shuffle lines
        elif args.filename is not None:
            generator.readFile(args.filename)
            generator.shuffle()
        
        # head count
        if args.head_count is not None:
            generator.head(args.head_count)

        # repeat
        if args.repeat:
            generator.repeat()
        else:
            generator.display()
                        
    except IOError as e:
        sys.exit()

if __name__ == "__main__":
    main()
