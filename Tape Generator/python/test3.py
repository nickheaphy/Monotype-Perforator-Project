from compcaster import Case
from compcaster import Wedge
from compcaster import Utils
from hyphenate import hyphenate_word

word = "chromatographic"

case_layout = "case_layout/layout161.txt"
case = Case.MatrixCase(case_layout)
wedge = Wedge.Wedge()

print(hyphenate_word(word))

print(Utils.besthypernation(hyphenate_word(word),case,wedge,500))