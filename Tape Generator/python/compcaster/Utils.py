'''
Some utility functions
'''
import logging
from hyphenate import hyphenate_word
from typing import Callable, Iterator, Union, Optional, List
from compcaster import Case
from compcaster import Wedge
import math

# create logger
module_logger = logging.getLogger('compcaster.Utils')

# ----------------------------------------------------------
def mm2picas(mm, pica = 0.1660):
    '''Convert mm to pica (default pica is 0.1660 (New British Pica)'''
    return round(float(mm)/25.4/pica)

# ----------------------------------------------------------
def wordwidth(word, case, wedge, style = None):
    '''Calculate the word width (excluding any spaces)'''
    width = 0
    for the_char in word:
        column, row = case.get_char(the_char, style)
        if row is not None:
            width += wedge.units[row]
        else:
            module_logger.error(f'Character {the_char} not found - skipping....')
    
    return width

# ----------------------------------------------------------
def width(chars, case, wedge, style = None):
    '''Calculate the width of the chars'''
    # this is just a convience function that uses wordwidth
    return wordwidth(chars, case, wedge, style)

# ----------------------------------------------------------
def besthyphenation(word: str, case: Case, wedge: Wedge, style: str, remainingspace: int) -> List:
    '''Find the longest option for hypernation into the available space (ie minimise
    the justification spaces required)
    Uses Frank Liang’s algorithm for hyphenation (used in TeX)
    http://www.tug.org/docs/liang/
    https://github.com/jfinkels/hyphenate

    Parameters:
        word - the word to check if it can be hyphenated
        case - the matrix case (Case class)
        wedge - the wedge being used for spacing (Wedge class)
        remainingspace - the amount of space available to try and fit the word into
    '''
    hyp_options = hyphenate_word(word)
    if len(hyp_options) > 1:
        return _besthyphenation(hyp_options,case,wedge,style,remainingspace)
    else:
        return ["", hyp_options[0]]

# ----------------------------------------------------------
def _besthyphenation(wordlist: List, case: Case, wedge: Wedge, style: str, remainingspace: int) -> List:
    '''Recursivly find the longest option for hypernation into the available space
    
    Parameters:
        wordlist - a list of the ways you can breakup a word (eg ['hy', 'phen', 'ation'])
        case - the matrix case
        wedge - the wedge being used for spacing
        style - the style of the word (eg None, s, i etc)
        remainingspace - the amount of space available to try and fit the word into
    '''
    #print(wordlist)
    if len(wordlist) > 1:
        theword = ''.join(wordlist[:-1]) + "-"
        #module_logger.debug(f"Testing Hypenation of Word: {theword}, {wordwidth(theword, case, wedge)}")
        if wordwidth(''.join(wordlist[:-1]) + "-", case, wedge, style) <= remainingspace:
            return [''.join(wordlist[:-1]) + "-", wordlist[-1]]
        else:
            #print()
            #print(''.join(wordlist[-2:]))
            new_wordlist = wordlist[:-2]
            new_wordlist.append(''.join(wordlist[-2:]))
            #print(new_wordlist)
            #print(wordlist[:-2].append(''.join(wordlist[-2:])))
            return _besthyphenation(new_wordlist, case, wedge, style, remainingspace)
    else:
        return ["", wordlist[0]]


# ------------------------------------------------------------
def draw(codes, the_char:str = None, comment:str = '', end:str = '\n'):
    '''Draw the codes suitable for punching
    
    Parameters:
        codes (List): a List of the punch codes to punch on this line
        the_char (str): optional text to printout on the line
        comment (str): optional text to printout on the line
        end (str): the line end

    This will look something like
    |----------o------------o-------| 'the_char' [codes] comment end
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
    print(f" {the_codes} {comment}", end=end)


# ------------------------------------------------------------
def intersperse(lst, item):
    '''Interspese a list with item'''
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result

# ------------------------------------------------------------
def roll_amount(length_mm: float):
    '''Calculate how much roll we need
    
    Paramters:
        length_mm (float): the length of tape we need (mm)

    Returns:
        diameter (float): the diameter of the tape (mm)
    '''
    # L = length of material
    # t = thickness
    # D = outside diameter
    # d = hole diameter

    # pi(D*D - d*d)/4 = L t
    # L = pi(D*D - d*d)/4t
    # D = SQRT((L4t/pi)+d*d)

    PAPER_THICKNESS_MM = 0.08 
    CORE_DIAMETER_MM = 22

    L = length_mm
    t = PAPER_THICKNESS_MM
    d = CORE_DIAMETER_MM

    D = math.sqrt((L*4*t/math.pi)+d*d)
    return D
