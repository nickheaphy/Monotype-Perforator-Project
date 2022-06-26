'''Check the case layout'''

# Imports
import sys
from typing import List, IO
from compcaster import Case
from compcaster import Wedge
from compcaster import Utils
import logging
import math
from hyphenate import hyphenate_word

#Globals
case_layout = ""

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

def main():
    '''Main Program'''
    logger.debug(f'Starting to Parse {case_layout}')
    case = Case.MatrixCase(case_layout)



# ------------------------------------------------------------
# Main body
if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        print('Please enter the case to check on the commandline')
    else:
        case_layout = sys.argv[1]
        main()