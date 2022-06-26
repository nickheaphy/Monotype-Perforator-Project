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
case_layout = "case_layout/layout32.txt"
galley_width_mm = 155
case = Case.MatrixCase(case_layout)
wedge = Wedge.Wedge('S536-11.25')
galley = Galley.Galley(galley_width_mm,case,wedge)
outputfolder = "./reference/sampleoutput/"


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


styles = case.list_styles()
tape_sets = [standard.standardCAPS, standard.standardLC, standard.standardNUMS_PUNCH]
tape_names = ["Capitals", "Lowercase", "Numbers&Punctuation"]

for style in styles:
    for i, ts in enumerate(tape_sets):
        sys.stdout = open(outputfolder + f"Garamond-{style}-{tape_names[i]}.txt",'w')
        print(f"Garamond 157 Fount (Chars={tape_names[i]}) (Style={style})")
        galley.galley_info()
        Tape.tape_begin()
        numlines = galley.style_fount_generator(style, ts, minimum=10, bonus=5)
        Tape.tape_end(numlines)

sys.stdout = open(outputfolder + f"Garamond-Extras.txt",'w')
print(f"Garamond 157 Fount (Chars=Extras)")
galley.galley_info()
Tape.tape_begin()
numlines = galley.individual_chars_generator(garamond156.garamond156, minimum=10, bonus=5)
Tape.tape_end(numlines)
