'''This is just reformating the paragraphs using hyphanaton'''

from compcaster import Case
from compcaster import Utils
from compcaster import Justify
from compcaster import Wedge
import logging
import math

logger = logging.getLogger('compcaster')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)

case_layout = "case_layout/layout161-alt.txt"

case = Case.MatrixCase(case_layout)
wedge = Wedge.Wedge('S536-9.5')

linewidth = Utils.mm2picas(100)
setsize = wedge.set_width
lowerlimit_vs = 4
normal_vs = 6
ONE_UNIT_OF_ONE_SET = 0.0007685 #inches
sig_0005 = 0.0005
sig_0075 = 0.0075
size_multipler = 12 #pica or 12.84 for cicero
units_of_set_per_line = linewidth * 12 * 18 / setsize

indent_quad = 4
sentence_space = 2

# tape lengths
per_line_length_mm = 64 / 20 # 64mm for 20 lines
leaders = 400 #400mm

# What are we generating
founddesc = "Small Caps Test"
# This is a list of lists, lists contain ['Character', 'Style', Quantity]
fount = [
    ['A','s',30],
    ['B','s',30],
    ['C','s',30],
    ['D','s',30],
    ['E','s',40],
    ['F','s',30],
    ['G','s',30],
    ['H','s',30],
    ['I','s',30],
    ['J','s',30],
    ['K','s',30],
    ['L','s',30],
    ['M','s',30],
    ['N','s',30],
    ['O','s',30],
    ['P','s',30],
    ['Q','s',30],
    ['R','s',30],
    ['S','s',30],
    ['T','s',30],
    ['U','s',30],
    ['V','s',30],
    ['W','s',30],
    ['X','s',30],
    ['Y','s',30],
    ['Z','s',30]
]
# ------------------------------------------------------------
def main():

    linecounter = 0

    print(f"Desc: {founddesc}")
    print(f"Case Layout: {case_layout}")
    print(f"Wedge: {wedge}")
    print(f"Wedge Units: {wedge.units[1:]}")
    print(f"Linelength: {linewidth} em")
    print(f"Setsize: {setsize}")
    print(f"Calc units of set per line: {units_of_set_per_line}")
    print(f"Fount [char, style, quantity]: {fount}")
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

    intersperse_found = intersperse(fount, [case.QUAD, None, 1])
    usedline = 0

    for char in intersperse_found:
        the_char = char[0]
        the_style = char[1]
        the_quantity = char[2]
        
        for i in range(the_quantity):

            # Request to have two quads at beginning of the line
            if usedline == 0:
                charwidth = Utils.wordwidth(case.QUAD, case, wedge)
                logger.debug(f"Beginning of line. Pre-allocating space for 4 quads ({4*charwidth})")
                column, row = case.get_char(case.QUAD)
                draw([str(column),str(row)], case.QUAD)
                linecounter += 1
                draw([str(column),str(row)], case.QUAD, "")
                linecounter += 1
                usedline = 4 * charwidth
                print(f" Quad Width: {charwidth}(each), Used {usedline} of {units_of_set_per_line}")

            charwidth = Utils.wordwidth(the_char, case, wedge, the_style)
            # do we have enough space on this line to fit this character?
            if (usedline + lowerlimit_vs + charwidth) <= units_of_set_per_line:
                # yes we do
                column, row = case.get_char(the_char,the_style)
                draw([str(column),str(row)], the_char, "")
                linecounter += 1
                usedline += charwidth
                print(f" Width: {charwidth}, Used: {usedline} of {units_of_set_per_line}")
            else:
                #no we don't
                numspaces = 0
                while usedline + lowerlimit_vs <= units_of_set_per_line:
                    # add as many justification spaces as we can to fill
                    column, row = case.get_char(' ')
                    draw(['S',str(column),str(row)], " ")
                    linecounter += 1
                    usedline += lowerlimit_vs
                    numspaces += 1

                # add two quads
                column, row = case.get_char(case.QUAD)
                draw([str(column),str(row)], case.QUAD)
                linecounter += 1
                draw([str(column),str(row)], case.QUAD)
                linecounter += 1

                logger.debug(f"Usedline: {usedline} of {units_of_set_per_line}")
                # perform justification
                justifyspaces(units_of_set_per_line - usedline, numspaces)
                linecounter += 2
                usedline = 0

    # we have run out of characters
    logger.debug(f"End of fount: Padding with quads and j-spaces")
    # need to pad the remaining line with quads and spaces then justify
    charwidth = Utils.wordwidth(case.QUAD, case, wedge)
    while usedline + charwidth + lowerlimit_vs <= units_of_set_per_line:
        # add as many quads as we can to fill
        column, row = case.get_char(case.QUAD)
        draw([str(column),str(row)], case.QUAD)
        linecounter += 1
        usedline += charwidth
    
    numspaces = 0
    while usedline + lowerlimit_vs <= units_of_set_per_line:
        # add as many justification spaces as we can to fill
        column, row = case.get_char(' ')
        draw(['S',str(column),str(row)], " ")
        linecounter += 1
        usedline += lowerlimit_vs
        numspaces += 1
    
    # add two quads
    column, row = case.get_char(case.QUAD)
    draw([str(column),str(row)], case.QUAD)
    linecounter += 1
    draw([str(column),str(row)], case.QUAD)
    linecounter += 1

    # now justify
    justifyspaces(units_of_set_per_line - usedline, numspaces)
    linecounter += 2

    print("Generate Trailing Space command")
    print(f"**f{leaders/per_line_length_mm:.0f}")
    print(f"**t4")
    linecounter += round(leaders/per_line_length_mm)
    # end
    print()
    print(f"Total Lines: {linecounter} (including leader and trailer)")
    print(f"Tape Length: {linecounter*per_line_length_mm:.0f} mm")


# ------------------------------------------------------------
def draw(codes, the_char = None: str, end = '\n': str):
    '''Draw the codes as a series of dots
    
    Parameters:
    codes (List): a List of the punch codes to punch on this line
    the_char (str): optional text to printout on the line
    end (str): the line end
    '''
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
def intersperse(lst, item):
    '''Interspese a list with item'''
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result

# ------------------------------------------------------------
def justifyspaces(total_space_remaining, numspaces):
    #total_space_remaining = units_of_set_per_line - usedline
    logger.debug(f"Unset Units: {total_space_remaining}")
    if numspaces > 0:
        interword_space = total_space_remaining / numspaces
    else:
        interword_space = 0
    units_of_set_to_add_to_spaces = interword_space + lowerlimit_vs - normal_vs
    logger.debug(f"Units of Set to add to {numspaces} j-spaces: {units_of_set_to_add_to_spaces}")
    total_required_0005_steps = round(units_of_set_to_add_to_spaces * size_multipler * (ONE_UNIT_OF_ONE_SET/sig_0005))
    logger.debug(f"total_required_0005\"_steps: {total_required_0005_steps} = round({units_of_set_to_add_to_spaces} * {size_multipler} * {(ONE_UNIT_OF_ONE_SET/sig_0005)})")

    if total_required_0005_steps + 53 <= 16 or total_required_0005_steps + 53 >= 240:
        print(f"ERROR: can't justify this amount. Quiting")
        exit()
    justification_0075 = (total_required_0005_steps + 53) // 15
    justification_0005 = (total_required_0005_steps + 53) % 15
    logger.debug(f"Justification: ({total_required_0005_steps} + 53) / 15 = {justification_0075}/{justification_0005}")
    
    draw(['0075', str(justification_0075)], "0075", "")
    print(f" Unset: {total_space_remaining:.1f}, Units to {numspaces} j-spaces: {units_of_set_to_add_to_spaces:.1f}, req_0005\"_steps: {total_required_0005_steps} = round({units_of_set_to_add_to_spaces:.1f} * {size_multipler} * {(ONE_UNIT_OF_ONE_SET/sig_0005)})")
    draw(['0005','0075', str(justification_0005)], "0005/0075", "")
    print(f" Justification: ({total_required_0005_steps} + 53) / 15 = {justification_0075}/{justification_0005}")



# Main body
if __name__ == '__main__':
    
    main()