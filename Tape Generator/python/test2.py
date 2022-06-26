#!/usr/bin/env python3 -tt
"""
Quick Test of 
"""

# Imports
import sys
from typing import List, IO
from compcaster import Case
from compcaster import Wedge
from compcaster import Utils
import logging
import math
from hyphenate import hyphenate_word

#import os

# Global variables
case_layout = "case_layout/layout161-alt.txt"
filepath = "reference/1984.txt"

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


# tape lengths
per_line_length_mm = 64 / 20 # 64mm for 20 lines
leaders = 400 #400mm

# Function declarations
# ------------------------------------------------------------
def main():
    '''Main Program'''
    logger.debug(f'Starting to Parse {case_layout}')
    case = Case.MatrixCase(case_layout)
    wedge = Wedge.Wedge('S536-9.5E')

    linelength = Utils.mm2picas(100)
    setsize = 9.5
    lowerlimit_vs = 4
    normal_vs = 6
    ONE_UNIT_OF_ONE_SET = 0.0007685 #inches
    sig_0005 = 0.0005
    sig_0075 = 0.0075
    size_multipler = 12 #pica or 12.84 for cicero
    units_of_set_per_line = linelength * 12 * 18 / setsize

    usedline = 0
    numspaces = 0
    linecounter = 0

    #print(f"Test Paragraph: {test_sentence}")
    #print(f"Desc: {founddesc}")
    print(f"Case Layout: {case_layout}")
    print(f"Wedge: {wedge}")
    print(f"Wedge Units: {wedge.units[1:]}")
    print(f"Linelength: {linelength} em")
    print(f"Setsize: {setsize}")
    print(f"Calc units of set per line: {units_of_set_per_line}")
    #print(f"Fount [char, style, quantity]: {fount}")
    print(f"Seperator: Quad, Postion: {case.get_char(case.QUAD)}")
    print(f"")
    print(f"Increase the speed of the punch...")
    print(f"**p30") #this is the post punch delay
    print(f"**d100") #this is the forward delay
    print(f"Send commands to test all the punches, then advance 400mm ({leaders/per_line_length_mm:.0f} linefeeds)")
    print(f"**t4")
    print(f"**t1")
    print(f"**f{leaders/per_line_length_mm:.0f}")
    linecounter += round(leaders/per_line_length_mm)
    print(f"Send the termination (this is the last command read by the Composition Caster")
    print(f"This is two additional ems and because the line is now too long it will stop")
    print(f"the caster. Need a 0075 and 0005 followed by a 0005")
    draw(['0005'], "0005")
    draw(['0005','0075'])
    column, row = case.get_char(case.QUAD)
    draw([str(column),str(row)], case.QUAD)
    draw([str(column),str(row)], case.QUAD)
    linecounter += 4

    #intersperse_found = intersperse(fount, [case.QUAD, None, 1])
    usedline = 0

    with open(filepath) as fp:
        for paragraph in fp:
            # split the paragraph into words (on the space)
            words = paragraph.strip().split(' ')

            logger.debug("Begin Paragraph")
            i=0
            while i < len(words):
                word = words[i]
                #print(f"Word: {word}")
                # need to ensure that the whole word will fit on the line
                # if there are already words in the line then ensure a space
                # is prepended
                if usedline == 0:
                    wordwidth = 0
                else:
                    wordwidth = lowerlimit_vs

                # for the_char in word:
                #     column, row = case.get_char(the_char)
                #     if row is not None:
                #         wordwidth += wedge.units[row]
                wordwidth += Utils.wordwidth(word, case, wedge)

                # can we fit this word (and maybe the space) into the line?
                if usedline + wordwidth < units_of_set_per_line:
                    if usedline != 0:
                        column, row = case.get_char(' ')
                        draw(['S',str(column),str(row)],"","")
                        print(f" {' '}: S {column} {row}")
                        numspaces += 1
                    for the_char in word:
                        column, row = case.get_char(the_char)
                        draw([str(column),str(row)],"","")
                        print(f" {the_char}: {column} {row}")
                    usedline += wordwidth
                    # increment word counter
                    i += 1
                elif Utils.besthyphenation(word,case,wedge,units_of_set_per_line-usedline-lowerlimit_vs)[0] != "":
                    logger.debug(f"Space remaining on line {round(units_of_set_per_line-usedline-lowerlimit_vs)} (picas)")
                    logger.debug(f"'{word}'' too big ({Utils.wordwidth(word, case, wedge)} picas)")
                    hypenation_options = Utils.besthyphenation(word,case,wedge,units_of_set_per_line-usedline-lowerlimit_vs)
                    wordwidth = Utils.wordwidth(hypenation_options[0], case, wedge)
                    logger.debug(f"Using hyphenation: '{hypenation_options[0]}' ({wordwidth} picas) and '{hypenation_options[1]}' ({Utils.wordwidth(hypenation_options[1], case, wedge)} picas)")
                    if usedline != 0:
                        column, row = case.get_char(' ')
                        draw(['S',str(column),str(row)],"","")
                        print(f" {' '}: S {column} {row}")
                        numspaces += 1
                    for the_char in hypenation_options[0]:
                        column, row = case.get_char(the_char)
                        draw([str(column),str(row)],"","")
                        print(f" {the_char}: {column} {row}")
                    usedline += wordwidth
                    # replace the current word with the hypenation and don't increament the counter
                    words[i] = hypenation_options[1]
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
                    draw(['0075', str(justification_0075)],"","")
                    print(f" 0075: {justification_0075}")
                    draw(['0005','0075', str(justification_0005)],"","")
                    print(f" 0005 0075: {justification_0005}")

                    # new line
                    for the_char in word:
                        column, row = case.get_char(the_char)
                        draw([str(column),str(row)])
                        print(f" {the_char}: {column} {row}")
                    usedline = wordwidth
                    numspaces = 0
                
                    # increment word counter
                    i += 1

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
# ------------------------------------------------------------
def draw(codes, the_char = None, end = '\n'):
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
    if the_char is not None:
        print(f" '{the_char}'", end='')
    print(f" {the_codes}", end=end)


# ------------------------------------------------------------
# Main body
if __name__ == '__main__':
    
    main()