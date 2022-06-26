'''
Classes around Justification
https://www.youtube.com/watch?v=Np_Y740aReI 
'''
from typing import TextIO, List, Tuple

ONE_UNIT_OF_ONE_SET = 0.0007685 #inches

# For testing, here is a default wedge
S5 = [5,6,7,8,9,9,9,10,10,11,12,13,14,15,18]
WEDGE = S5

LOWERLIMIT_VSPACE = 4
NORMAL_VSPACE = 6

class Justifytext:
    ''' 
    '''
    # To justify text you need to know:
    # Line Length
    #   Need to convert the line length into units of set. This conversion
    #   will be dependant on the measurement units. The monotype programing
    #   book uses pica ems
    # Set Size
    #   Set is the width of the character (which changes based on the character)
    #   The fount set size is generally the width of the largest character in
    #   in the found.
    #   Individual characters are classifed as being divisible by 18 units eg
    #   the i would be 5 units of set and the W being 18 units of set (ie the
    #   Set Size)
    #   Any fount can have up with 15 different unit-widths (with some exceptions)
    #   which is defined as part of the wedge
    # Wedge Unit Values
    #   The wedge defines the width of each of the rows in the Matrix Case in
    #   units of set
    pass
    