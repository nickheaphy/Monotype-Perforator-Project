#!/usr/bin/env python3 -tt
"""
Quick Test of 
"""

# Imports
import sys
from typing import List, IO
from compcaster import Case
from compcaster import Wedge
import logging
import math

#import os

# Global variables
case_layout = "case_layout/layout161.txt"

logger = logging.getLogger('compcaster')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)
# Class declarations

# Function declarations
# ------------------------------------------------------------
def main():
    '''Main Program'''
    logger.debug(f'Starting to Parse {case_layout}')
    case = Case.MatrixCase(case_layout)
    wedge = Wedge.Wedge()

    test_sentence = "The Quick Brown Fox jumps over the Lazy Dog."
    #test_sentence = "The quick brown fox"
        

    # testing justifications
    #S5 = [5,6,7,8,9,9,9,10,10,11,12,13,14,15,18]
    #S5 = [0] + S5 #this just makes the referencing easier
    S5 = [0,5,6,7,8,9,9,10,10,11,12,13,14,15,17,19]
    linelength = 10 #pica ems
    setsize = 11.25
    lowerlimit_vs = 4
    normal_vs = 6
    ONE_UNIT_OF_ONE_SET = 0.0007685 #inches
    sig_0005 = 0.0005
    sig_0075 = 0.0075
    size_multipler = 12 #pica or 12.84 for cicero
    units_of_set_per_line = linelength * 12 * 18 / setsize

    usedline = 0
    numspaces = 0

    print(f"Test Paragraph: {test_sentence}")
    print(f"Wedge IO: {S5}")
    print(f"Linelength: {linelength}")
    print(f"Setsize: {setsize}")
    print(f"Calc units of set per line: {units_of_set_per_line}")

    # split the paragraph into words (on the space)
    words = test_sentence.split(' ')

    for word in words:
        # need to ensure that the whole word will fit on the line
        # if there are already words in the line then ensure a space
        # is prepended
        if usedline == 0:
            wordwidth = 0
        else:
            wordwidth = lowerlimit_vs

        for the_char in word:
            column, row = case.get_char(the_char)
            wordwidth += S5[row]

        # can we fit this word (and maybe the space) into the line?
        if usedline + wordwidth < units_of_set_per_line:
            if usedline != 0:
                column, row = case.get_char(' ')
                draw(['S',str(column),str(row)])
                print(f" {' '}: S {column} {row}")
                numspaces += 1
            for the_char in word:
                column, row = case.get_char(the_char)
                draw([str(column),str(row)])
                print(f" {the_char}: {column} {row}")
            usedline += wordwidth
        else:
            # no we can't, so need to justify the space
            # remaining and put the word onto the next line
            # justify and new line
            total_space_remaining = units_of_set_per_line - usedline
            if numspaces > 0:
                interword_space = total_space_remaining / numspaces
            else:
                interword_space = 0
            units_of_set_to_add_to_spaces = interword_space + lowerlimit_vs - normal_vs
            total_required_0005_steps = round(units_of_set_to_add_to_spaces * size_multipler * (ONE_UNIT_OF_ONE_SET/sig_0005))
            justification_0075 = math.floor((total_required_0005_steps + 53) / 15)
            justification_0005 = (total_required_0005_steps + 53) % 15
            #print(f"**** New Line ****")
            #print(f"Used units of set: {usedline}")
            #print(f"Spaces: {numspaces}")
            #print(f"0075: {justification_0075} 0005: {justification_0005}")
            draw(['0075', str(justification_0075)])
            print(f" 0075: {justification_0075}")
            draw(['0005','0075', str(justification_0005)])
            print(f" 0005 0075: {justification_0005}")

            # new line
            for the_char in word:
                column, row = case.get_char(the_char)
                draw([str(column),str(row)])
                print(f" {the_char}: {column} {row}")
            usedline = wordwidth
            numspaces = 0

    # end of paragraph. Justify
    total_space_remaining = units_of_set_per_line - usedline
    if numspaces > 0:
        interword_space = total_space_remaining / numspaces
    else:
        interword_space = 0
    units_of_set_to_add_to_spaces = interword_space + lowerlimit_vs - normal_vs
    total_required_0005_steps = round(units_of_set_to_add_to_spaces * size_multipler * (ONE_UNIT_OF_ONE_SET/sig_0005))
    justification_0075 = math.floor((total_required_0005_steps + 53) / 15)
    justification_0005 = (total_required_0005_steps + 53) % 15
    #print(f"**** New Line ****")
    #print(f"Used units of set: {usedline}")
    #print(f"Spaces: {numspaces}")
    #print(f"0075: {justification_0075} 0005: {justification_0005}")
    draw(['0075', str(justification_0075)])
    print(f" 0075: {justification_0075}")
    draw(['0005','0075', str(justification_0005)])
    print(f" 0005 0075: {justification_0005}")



# ------------------------------------------------------------
def draw(codes):
    '''Draw the codes as a series of dots'''
    # the codes will be a series of letters and numbers
    punchpositions = ['N','M','L','K','J','I','H','G','F','S','E','D','0075','C','B','A',
        '1','2','3','4','5','6','7','8','9','10','11','12','13','14','0005']
    fullpunch = ''.ljust(31,'-') #string of 31 spaces
    if isinstance(codes, list):
        the_codes = codes
    else:
        the_codes = codes.split(' ')
    for code in the_codes:
        try:
            pos = punchpositions.index(code)
            string_list = list(fullpunch) 
            string_list[pos] = 'o'
            fullpunch = "".join(string_list)
        except:
            pass
    
    print(f"|{fullpunch}|", end='')


# ------------------------------------------------------------
# Main body
if __name__ == '__main__':
    
    main()