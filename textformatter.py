# Lambert SU
# V00851073

#!/usr/bin/python3

# file        : textformatter.py
# what to do  : format strings
# date        : Nov 15th, 2016


import fileinput
import sys


class Formatter:
    #class to format file or str list

    def __init__(self, inputfile, strs):
        self.inputfile = inputfile
        self.strs = strs

        # constant variables for command
        # modified this to class member instead global variable
        self.constant = {
            '.FT': False,
            '.LW': 0,
            '.LM': 0,
            '.LS': 0,
            'line_length': 0,
        }

    def get_lines(self):
        try:
            # read each line from input file
            lines = self.strs if self.strs else [line for line in fileinput.input()]
            # formatted each line if not empty line
            formatted = [self.format(line) for line in lines]
            format_line = [line for line in formatted if line]

            return ''.join(format_line).split('\n')
        except IOError :
	    # error case: not able to open file
            print('Not able to open non exist file', self.inputfile)
            sys.exit()

    def format(self, line):

        # split each line in the file
        seperate = line.split()
        # not empty, check for the command
        if len(seperate) != 0:

            if seperate[0] == ".FT":
                if seperate[1] == "on":
                    self.constant['.FT'] = True
                else:
                    #format is off
                    self.constant['.FT'] = False

                return None

            elif seperate[0] == ".LW":
                try:
                    # get the number right after '.LW'
                    self.constant['.LW'] = int(seperate[1])
                    #format is on
                    self.constant['.FT'] = True
                    # check for signs (positive or negative)
                    if seperate[1][0] == '-':
                        # get the number right after signs('-' or '+')
                        self.constant['.LW'] -= int(seperate[1][1:])

                    elif seperate[1][0] == '+':
                        self.constant['.LW'] += int(seperate[1][1:])

                    return None
                except ValueError:
                    # error case : invalid input
                    print('Format error, value LW must be an integer and a digit,')
                    sys.exit(-1)

            elif seperate[0] == ".LM":
                try:
                    self.constant['.LM'] = int(seperate[1])

                    if seperate[1][:1] == "-":
                        self.constant['.LM'] -= int(seperate[1][1:])

                    # .LM must be > 0

                        self.constant['.LM'] = max(0, self.constant['.LM'])

                    elif seperate[1][:1] == "+":
                        self.constant['.LM'] += int(seperate[1][1:])

                    # .LM must be < '.LW' - 20
                    self.constant['.LM'] = min(
                        self.constant['.LW'] - 20, self.constant['.LM'])

                    return None
                except ValueError:
                    print('Format error, value LM must be an integer and a digit,')
                    sys.exit(-1)

            elif seperate[0] == ".LS":
                try:
                    self.constant['.LS'] = int(seperate[1])
                    if self.constant['.LS'] > 2 or self.constant['.LS'] < 0:
                        print('Format error, LS value must between 0 to 2,', self.constant['.LS'],'is not valid' )
                        sys.exit(-1)
                    return None
                except ValueError:
                    print('Format error, LS value must be an integer and a digit,')
                    sys.exit(-1)
        # format is on, print format lines
        if self.constant['.FT']:

            # check spaces and margins first
            if self.constant['line_length'] == 0:

                left_mrgn = (' ' * self.constant['.LM'])
                space = ('\n' * self.constant['.LS'])
                formatline = "" + space + left_mrgn
                # set current line_length to left margin length
                # line_length should be 0 if no 'LM' command
                self.constant['line_length'] = self.constant['.LM']
            else:
                formatline = ""

            # new lines for empty line
            if seperate == []:
                self.constant['line_length'] = 0
                return "\n\n"

            for splits in seperate:

                # comparision first if exceed the LW
                if self.constant['line_length'] + len(splits) >= self.constant['.LW']:

                    # add margins and spaces for each line if needed
                    left_mrgn = (' ' * self.constant['.LM'])
                    space = ('\n' * self.constant['.LS'])
                    formatline = formatline + space + '\n' + left_mrgn
                    # set current line_length to LM after line comparision
                    # current line_length should be 0 if no LM command
                    self.constant['line_length'] = self.constant['.LM']

                # add space at the end for each lines
                elif self.constant['line_length'] > self.constant['.LM']:
                    self.constant['line_length'] += 1
                    formatline = formatline + ' '
                # add each word to format line
                formatline = formatline + splits
                self.constant['line_length'] += len(splits)
            return formatline
        else:
            return line