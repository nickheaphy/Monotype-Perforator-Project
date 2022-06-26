''' Tape Utils'''
from compcaster import Utils

# tape lengths
per_line_length_mm = 64 / 20 # 64mm for 20 lines
lead_in_out = 400 # 400mm leaders

# ------------------------------------------------------
def tape_begin() -> None:
    print(f"")
    print(f"Increase the speed of the punch...")
    print(f"**p30") #this is the post punch delay
    print(f"**d100") #this is the forward delay
    print(f"Send commands to test all the punches, then advance {lead_in_out}mm ({lead_in_out/per_line_length_mm:.0f} linefeeds)")
    print(f"**t4")
    print(f"**f{lead_in_out/per_line_length_mm:.0f}")

# ------------------------------------------------------
def tape_end(numlines: int) -> None:
    print("Generate Trailing Space command")
    print(f"**f{lead_in_out/per_line_length_mm:.0f}")
    print(f"**t4")

    numlines += 2 * round(lead_in_out/per_line_length_mm)

    # end
    print()
    print(f"Total Tape Lines: {numlines} (including leader and trailer)")
    print(f"Tape Length: {numlines*per_line_length_mm:.0f} mm")
    print(f"Roll Diameter Required: {Utils.roll_amount(numlines*per_line_length_mm):.0f}mm")
    print()
    print()
