'''This is just reformating the paragraphs using hyphanaton'''

from compcaster import Case
from compcaster import Utils
from compcaster import Justify

textfile = "reference/1984.txt"

case_layout = "case_layout/layout161.txt"

case = Case.MatrixCase(case_layout)

wedge = [0,5,6,7,8,9,9,10,10,11,12,13,14,15,17,19]

linewidth = Utils.mm2picas(200)
setsize = 11.25
lowerlimit_vs = 4
normal_vs = 6
ONE_UNIT_OF_ONE_SET = 0.0007685 #inches
sig_0005 = 0.0005
sig_0075 = 0.0075
size_multipler = 12 #pica or 12.84 for cicero
units_of_set_per_line = linewidth * 12 * 18 / setsize

indent_quad = 4
sentence_space = 2

# ------------------------------------------------------------
def main():
    print(f"Wedge IO: {wedge}")
    print(f"Linelength: {linewidth} em")
    print(f"Setsize: {setsize}")
    print(f"Calc units of set per line: {units_of_set_per_line}")
    with open(textfile) as fp:
        for paragraph in fp:
            paragraph = paragraph.strip()
            if len(paragraph) > 1:
                words = paragraph.split(' ')
                line = []
                for i, word in enumerate(words):
                    if i == 0:
                        #begining of the paragraph, do we need to indent?
                        if indent_quad > 0:
                            line.append(case.QUAD * indent_quad)
                    # do we have space to append the word
                    if space_for_space_and_word(word, line, linewidth, case, wedge):
                        # yes, so appeand a space and the word
                        line.append(word)
                        line.append(' ')
                    # do we have space to appeand the word without a space?
                    elif space_for_word(word, line, linewidth, case, wedge):
                        line.append(word)


                    print(f"Word: {word} Width: {word_width(word, case, wedge)}")



# ------------------------------------------------------------
def fix_spaces(paragraph, indent, sentence_space):
    pass

# ------------------------------------------------------------
def word_width(word, case, wedge):
    '''Calculate the width of a word using a case and a wedge'''
    wordwidth = 0
    for the_char in word:
        column, row = case.get_char(the_char)
        if row is not None:
            wordwidth += wedge[row]
    return wordwidth

# ------------------------------------------------------------
def line_width(linearray, case, wedge):
    totallinelength = 0
    for word in linearray:
        if word == ' ':
            totallinelength += lowerlimit_vs
        else:
            totallinelength += word_width(word, case, wedge)
    return totallinelength

# ------------------------------------------------------------
def space_for_space_and_word(word, linearray, linewidth, case, wedge):
    '''Is there space in the linearray to add the word?'''
    if lowerlimit_vs + word_width(word, case, wedge) + line_width(linearray,case,wedge) <= linewidth:
        return True
    else:
        return False
# ------------------------------------------------------------
def space_for_word(word, linearray, linewidth, case, wedge):
    '''Is there space in the linearray to add the word?'''
    if word_width(word, case, wedge) + line_width(linearray,case,wedge) <= linewidth:
        return True
    else:
        return False
# ------------------------------------------------------------
# Main body
if __name__ == '__main__':
    
    main()