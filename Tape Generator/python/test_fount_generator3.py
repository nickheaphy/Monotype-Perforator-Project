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

# ----------------------------------
# Parameters
case_layout = "case_layout/layout32.txt"
galley_width_mm = 155

# tape lengths
per_line_length_mm = 64 / 20 # 64mm for 20 lines
lead_in_out = 400 # 400mm leaders

case = Case.MatrixCase(case_layout)
wedge = Wedge.Wedge('S536-11.25')
galley = Galley.Galley(galley_width_mm,case,wedge)

style = 'i'

founddesc = f"Garamond 157 Fount (Style={style})"


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


print("")
print(f"Desc: {founddesc}")
galley.galley_info()
print(f"")
print(f"Increase the speed of the punch...")
print(f"**p30") #this is the post punch delay
print(f"**d100") #this is the forward delay
print(f"Send commands to test all the punches, then advance {lead_in_out}mm ({lead_in_out/per_line_length_mm:.0f} linefeeds)")
print(f"**t4")
print(f"**f{lead_in_out/per_line_length_mm:.0f}")

numlines = galley.style_fount_generator(style, standard.standard, minimum=10, bonus=5)
#numlines = galley.fount_generator(standard.standard, minimum=10, bonus=5)


print("Generate Trailing Space command")
print(f"**f{lead_in_out/per_line_length_mm:.0f}")
print(f"**t4")

numlines += 2 * round(lead_in_out/per_line_length_mm)

# end
print()
print(f"Total Tape Lines: {numlines} (including leader and trailer)")
print(f"Tape Length: {numlines*per_line_length_mm:.0f} mm")
print(f"Roll Diameter Required: {Utils.roll_amount(numlines*per_line_length_mm):.0f}mm")