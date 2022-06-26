# Just casts one of each character in a 15x15 block
# This was John Nixons request for testing border matrix's

from compcaster import Case
from compcaster import Utils
from compcaster import Justify
from compcaster import Wedge
from compcaster import Galley
import logging
import sys
import math
from fount_layouts import standard
from fount_layouts import garamond156
from compcaster import Tape

# ----------------------------------
# Parameters



# -------- Logging Setup -----------
logger = logging.getLogger('compcaster')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)
# -----------------------------------

xpos = ['A','B','C','D','E','F','H','I','J','K','L','M','N','O']
ypos = 15

Tape.tape_begin()
Utils.draw(['0075', '3'], "0075")
Utils.draw(['0005','0075', '8'], "0005/0075")
Utils.draw(['O', '15'], "")
Utils.draw(['O', '15'], "")

for y in range(1,ypos+1):
    for x in xpos:
    
        Utils.draw([x,str(y)])
    
    Utils.draw(['0075', '3'], "0075")
    Utils.draw(['0005','0075', '8'], "0005/0075")

lines = 15 * 19

Tape.tape_end(lines)
