'''
Galley class generates the justifed galley
'''

from typing import TextIO, List, Tuple
import logging
import unicodedata
import re
from compcaster import Case
from compcaster import Utils
from compcaster import Wedge

# create logger
module_logger = logging.getLogger('compcaster.Galley')

# -------------------------------------------------------------------------------
class Galley:
    
    ONE_UNIT_OF_ONE_SET = 0.0007685 #inches
    SIG_0005 = 0.0005 #width of a 0005 signal
    SIG_0075 = 0.0075 #width of a 0007 signal
    SIZE_MULTIPLIER = 12

    def __init__(self, width_mm: int, case: Case, wedge: Wedge) -> None:
        '''Build a galley of type

        Parameters:
        width_mm (int): the width of the galley in mm
        case (Case): the Case class that the text will be generated using
        wedge (Wedge): the Wedge class that the case will be using
        '''
        self.case = case
        self.wedge = wedge

        self.linewidth = Utils.mm2picas(width_mm,wedge.pica)
        self.linewidth_mm = width_mm

        self.setsize = wedge.set_width
        # Default space sizes
        self.lowerlimit_space = 4 #units of set
        self.normal_space = 6 #units of set
        
        #size_multipler = 12 #pica or 12.84 for cicero
        self.units_of_set_per_line = self.linewidth * 12 * 18 / self.setsize

    



    # ------------------------------------------------------------
    def DEPRECATED_fount_generator(self, char_list: List, pos_list: List = None, minimum: int = 0, bonus: int = 0) -> int:
        '''Generate a found
        
        ***** DEPRECATED ******
        This generates too long a tape as generates all styles on the same tape
        Use style_fount_generator instead
        ***********************

        Parameters:
            char_list (List): a list of Lists of the characters and quantities (eg [['a',10],['b',5]])
            pos_list (List): a list of Lists of the positions and quantity (eg [['N15',10],['A4',5]])
            minimum (int): the minimum quantity of each character to cast
            bonus (int): additional characters to each to cast

        The idea behind the pos_list is to generate character by their positon in the MCA
        for when the standard fount list does not contain the characters (eg special symbols etc)
        '''
        # some variables that we will use
        usedline = 0 # how much of the line have we used?
        missing_chars = 0 # how many missing characters did we hit?
        linecounter = 0 # how many lines of tape are we going to use?

        # to make life easier for the person casting the galley we are going to pad each line
        # with four quads (2 at beginning and end), this helps to ensure that the sorts don't fall over
        quad_column, quad_row = self.case.get_char(self.case.QUAD)
        quadwidth = Utils.width(self.case.QUAD, self.case, self.wedge)
        units_of_set_per_line = self.units_of_set_per_line - 4 * quadwidth

        # we are also going to interperse the characters with quads to make it easy to see them
        if pos_list is not None:
            char_list = Utils.intersperse(pos_list + char_list,[self.case.QUAD, 1, None, "PAD"])
        else:
            char_list = Utils.intersperse(char_list,[self.case.QUAD, 1, None, "PAD"])
        # What are the styles that are available in the case
        styles = self.case.list_styles()

        # Begin the tape with the stop commands
        self.stop_casting()

        for style in styles:
            # We are going to generate a fount of each style
            i = 0
            while i < len(char_list):
                the_char = char_list[i][0]
                the_quantity = minimum + bonus if char_list[i][1] < minimum else char_list[i][1] + bonus
                # if a style is supplied, use that
                if len(char_list[i]) >= 3:
                    the_style = char_list[i][2]
                else:
                    the_style = style
                if len(char_list[i]) >= 4:
                    if char_list[i][3] == "PAD":
                        the_quantity = 1

                j = 0
                while j < the_quantity:

                    # Does the character exist?
                    column, row = self.case.get_char(the_char,the_style)
                    if column is not None and row is not None:

                        if usedline == 0:
                            # Cast the initial 2 quads
                            Utils.draw([str(quad_column),str(quad_row)], self.case.QUAD)
                            Utils.draw([str(quad_column),str(quad_row)], self.case.QUAD)
                            linecounter += 2

                        #charwidth = Utils.width(the_char, self.case, self.wedge, the_style)
                        charwidth = self.wedge.units[row]
                        # do we have enough space on this line to fit this character?
                        if (usedline + self.lowerlimit_space + charwidth) <= units_of_set_per_line:
                            # yes we do
                            #column, row = case.get_char(the_char,the_style)
                            comment = f" Width: {charwidth}, Used: {usedline} of {units_of_set_per_line:.1f}"
                            Utils.draw([str(column),str(row)], the_char, comment)
                            linecounter += 1
                            usedline += charwidth
                        else:
                            #no we don't
                            numspaces = 0
                            while usedline + self.lowerlimit_space <= units_of_set_per_line:
                                # add as many justification spaces as we can to fill
                                column, row = self.case.get_char(' ')
                                Utils.draw(['S',str(column),str(row)], " ", "Justification Space")
                                linecounter += 1
                                usedline += self.lowerlimit_space
                                numspaces += 1

                            # add two quads
                            Utils.draw([str(quad_column),str(quad_row)], self.case.QUAD)
                            Utils.draw([str(quad_column),str(quad_row)], self.case.QUAD)
                            linecounter += 2

                            module_logger.debug(f"Usedline: {usedline} of {units_of_set_per_line}")
                            # perform justification
                            self.justifyspaces(units_of_set_per_line - usedline, numspaces)
                            linecounter += 2
                            usedline = 0

                        j += 1
                        
                    else:
                        # character does not exist, break out of the loop that is printing
                        # this character
                        missing_chars += 1
                        # skip the following character (as this will be another quad)
                        i += 1
                        j = the_quantity + 1
                        module_logger.debug(f"No char i:{i}/{len(char_list)}, j:{j}")

                # move to the next character
                i += 1
        
        # we have run out of characters
        module_logger.debug(f"End of fount: Padding line with quads and j-spaces")
        # need to pad the remaining line with quads and spaces then justify
        charwidth = Utils.width(self.case.QUAD, self.case, self.wedge)
        while usedline + charwidth + self.lowerlimit_space <= units_of_set_per_line:
            # add as many quads as we can to fill
            Utils.draw([str(quad_column),str(quad_row)], self.case.QUAD)
            linecounter += 1
            usedline += charwidth
        
        numspaces = 0
        while usedline + self.lowerlimit_space <= units_of_set_per_line:
            # add as many justification spaces as we can to fill
            column, row = self.case.get_char(' ')
            Utils.draw(['S',str(column),str(row)], " ")
            linecounter += 1
            usedline += self.lowerlimit_space
            numspaces += 1
        
        # add two quads
        Utils.draw([str(quad_column),str(quad_row)], self.case.QUAD)
        Utils.draw([str(quad_column),str(quad_row)], self.case.QUAD)
        linecounter += 2

        # now justify
        self.justifyspaces(units_of_set_per_line - usedline, numspaces)
        linecounter += 2

        return linecounter


    # ------------------------------------------------------------
    def style_fount_generator(self, style: str, char_list: List, minimum: int = 0, bonus: int = 0) -> int:
        '''Generate a fount
        
        Parameters:
            style (str): the style from the matrix you want to generate
            char_list (List): a list of Lists of the characters and quantities (eg [['a',10],['b',5]])
            minimum (int): the minimum quantity of each character to cast
            bonus (int): additional characters to each to cast

        Returns:
            linecounter (int): the number of lines cast
        '''
        # some variables that we will use
        usedline = 0 # how much of the line have we used?
        missing_chars = 0 # how many missing characters did we hit?
        linecounter = 0 # how many lines of tape are we going to use?
        galleyrows = 0 # how many lines of text do we have on the galley?

        # to make life easier for the person casting the galley we are going to pad each line
        # with four quads (2 at beginning and end), this helps to ensure that the sorts don't fall over
        quad_column, quad_row = self.case.get_char(self.case.QUAD)
        quadwidth = Utils.width(self.case.QUAD, self.case, self.wedge)
        units_of_set_per_line = self.units_of_set_per_line - 4 * quadwidth

        # we are also going to interperse the characters with quads to make it easy to see them
        char_list = Utils.intersperse(char_list,[self.case.QUAD, 1, None, "PAD"])

        # check that the requested style is valid
        if style not in self.case.list_styles():
            module_logger.error(f"Style '{style}' requested not available in matrix {self.case.list_styles()}")
            return linecounter

        # Begin the tape with the stop commands
        self.stop_casting()

        i = 0
        while i < len(char_list):
            the_char = char_list[i][0]
            the_quantity = minimum + bonus if char_list[i][1] < minimum else char_list[i][1] + bonus
            # if a style is supplied, use that
            if len(char_list[i]) >= 3:
                the_style = char_list[i][2]
            else:
                the_style = style
            if len(char_list[i]) >= 4:
                if char_list[i][3] == "PAD":
                    the_quantity = 1

            j = 0
            while j < the_quantity:

                # Does the character exist?
                column, row = self.case.get_char(the_char,the_style)
                if column is not None and row is not None:

                    if usedline == 0:
                        # Cast the initial 2 quads
                        Utils.draw([str(quad_column),str(quad_row)], self.case.QUAD)
                        Utils.draw([str(quad_column),str(quad_row)], self.case.QUAD)
                        linecounter += 2

                    #charwidth = Utils.width(the_char, self.case, self.wedge, the_style)
                    charwidth = self.wedge.units[row]
                    # do we have enough space on this line to fit this character?
                    if (usedline + self.lowerlimit_space + charwidth) <= units_of_set_per_line:
                        # yes we do
                        #column, row = case.get_char(the_char,the_style)
                        comment = f" Width: {charwidth}, Used: {usedline} of {units_of_set_per_line:.1f}"
                        Utils.draw([str(column),str(row)], the_char, comment)
                        linecounter += 1
                        usedline += charwidth
                    else:
                        #no we don't
                        numspaces = 0
                        while usedline + self.lowerlimit_space <= units_of_set_per_line:
                            # add as many justification spaces as we can to fill
                            column, row = self.case.get_char(' ')
                            Utils.draw(['S',str(column),str(row)], " ", "Justification Space")
                            linecounter += 1
                            usedline += self.lowerlimit_space
                            numspaces += 1

                        # add two quads
                        Utils.draw([str(quad_column),str(quad_row)], self.case.QUAD)
                        Utils.draw([str(quad_column),str(quad_row)], self.case.QUAD)
                        linecounter += 2

                        module_logger.debug(f"Usedline: {usedline} of {units_of_set_per_line}")
                        # perform justification
                        self.justifyspaces(units_of_set_per_line - usedline, numspaces)
                        galleyrows += 1
                        linecounter += 2
                        usedline = 0

                    j += 1
                    
                else:
                    # character does not exist, break out of the loop that is printing
                    # this character
                    missing_chars += 1
                    # skip the following character (as this will be another quad)
                    i += 1
                    j = the_quantity + 1
                    module_logger.debug(f"No char i:{i}/{len(char_list)}, j:{j}")

            # move to the next character
            i += 1
        
        # we have run out of characters
        module_logger.debug(f"End of fount: Padding line with quads and j-spaces")
        # need to pad the remaining line with quads and spaces then justify
        charwidth = Utils.width(self.case.QUAD, self.case, self.wedge)
        while usedline + charwidth + self.lowerlimit_space <= units_of_set_per_line:
            # add as many quads as we can to fill
            Utils.draw([str(quad_column),str(quad_row)], self.case.QUAD)
            linecounter += 1
            usedline += charwidth
        
        numspaces = 0
        while usedline + self.lowerlimit_space <= units_of_set_per_line:
            # add as many justification spaces as we can to fill
            column, row = self.case.get_char(' ')
            Utils.draw(['S',str(column),str(row)], " ")
            linecounter += 1
            usedline += self.lowerlimit_space
            numspaces += 1
        
        # add two quads
        Utils.draw([str(quad_column),str(quad_row)], self.case.QUAD)
        Utils.draw([str(quad_column),str(quad_row)], self.case.QUAD)
        linecounter += 2

        # now justify
        self.justifyspaces(units_of_set_per_line - usedline, numspaces)
        linecounter += 2
        galleyrows +=1 

        module_logger.info(f"Total Galley Rows = {galleyrows}")
        return linecounter


    def individual_chars_generator(self, pos_list: List = None, minimum: int = 0, bonus: int = 0) -> int:
        '''Generate a found
        
        Parameters:
            pos_list (List): a list of Lists of the positions and quantity (eg [['N15',10],['A4',5]])
            minimum (int): the minimum quantity of each character to cast
            bonus (int): additional characters to each to cast

        The idea behind the pos_list is to generate character by their positon in the MCA
        for when the standard fount list does not contain the characters (eg special symbols etc)

        This actually uses a feature of the MCA lookup that falls back to checking if we have
        passed a coordinate reference.
        '''
        return self.style_fount_generator(None, pos_list, minimum, bonus)


    # ------------------------------------------------------------
    def stop_casting(self):
        '''Print the stop casting commands'''
        # Send the termination (this is the last command read by the Composition Caster")
        # This is two additional ems and because the line is now too long it will stop")
        # the caster. Need a 0075 and 0005 followed by a 0005")
        Utils.draw(['0005'], "0005", "Caster Stopping")
        Utils.draw(['0005','0075'], "0005/0075", "Caster Stopping")
        column, row = self.case.get_char(self.case.QUAD)
        Utils.draw([str(column),str(row)], self.case.QUAD, "Caster Stopping")
        Utils.draw([str(column),str(row)], self.case.QUAD, "Caster Stopping")

    # ------------------------------------------------------------
    def galley_info(self):
        '''Print information about the galley'''
        print(f"Case Layout: {self.case.caselayout}")
        print(f"Wedge: {self.wedge}")
        print(f"Wedge Units: {self.wedge.units[1:]}")
        print(f"Galley Width: {self.linewidth} pica ({self.linewidth_mm}mm)")
        print(f"Setsize: {self.setsize}")
        print(f"Calc units of set per line: {self.units_of_set_per_line}")
        #print(f"Fount [char, style, quantity]: {fount}")
        print(f"Quad: Position: {self.case.get_char(self.case.QUAD)}")
        print(f"Jspace: Position: {self.case.get_char(self.case.JSPACE)}")


    # ------------------------------------------------------------
    def justifyspaces(self, total_space_remaining: float, numspaces: int):
        '''Draw the justification spaces

        Parameters:
            total_space_remaining (float): the units of set that is remaining
            numspaced (int): the number of spaces in the line
        '''
        
        module_logger.debug(f"Unset Units: {total_space_remaining}")

        if total_space_remaining > 0:
            if numspaces > 0:
                interword_space = total_space_remaining / numspaces
            else:
                interword_space = 0
            
            units_of_set_to_add_to_spaces = interword_space + self.lowerlimit_space - self.normal_space
            module_logger.debug(f"Units of Set to add to {numspaces} j-spaces: {units_of_set_to_add_to_spaces}")
            
            total_required_0005_steps = round(units_of_set_to_add_to_spaces * self.SIZE_MULTIPLIER * (self.ONE_UNIT_OF_ONE_SET/self.SIG_0005))
            module_logger.debug(f"total_required_0005\"_steps: {total_required_0005_steps} = round({units_of_set_to_add_to_spaces} * {self.SIZE_MULTIPLIER} * {(self.ONE_UNIT_OF_ONE_SET/self.SIG_0005)})")

            if total_required_0005_steps + 53 <= 16 or total_required_0005_steps + 53 >= 240:
                print(f"total_required_0005_steps: {total_required_0005_steps}")
                print(f"ERROR: can't justify this amount. Quiting")
                exit()
            justification_0075 = (total_required_0005_steps + 53) // 15
            justification_0005 = (total_required_0005_steps + 53) % 15
            module_logger.debug(f"Justification: ({total_required_0005_steps} + 53) / 15 = {justification_0075}/{justification_0005}")
            
            comment = f" Unset: {total_space_remaining:.1f}, Units to {numspaces} j-spaces: {units_of_set_to_add_to_spaces:.1f}, req_0005\"_steps: {total_required_0005_steps} = round({units_of_set_to_add_to_spaces:.1f} * {self.SIZE_MULTIPLIER} * {(self.ONE_UNIT_OF_ONE_SET/self.SIG_0005)})"
            Utils.draw(['0075', str(justification_0075)], "0075", comment)
            
            comment = f" Justification: ({total_required_0005_steps} + 53) / 15 = {justification_0075}/{justification_0005}"
            Utils.draw(['0005','0075', str(justification_0005)], "0005/0075", comment)
        
        else:
            # 1/1 justification
            Utils.draw(['0075', "1"], "0075", "1/1 justification")
            Utils.draw(['0005','0075', "1"], "0005/0075", "1/1 justification")

    # ------------------------------------------------------------
    def paragraph_generator(self, paragraph: str, style: str = None) -> int:
        '''Generate a paragraph of punches

        Parameters:
            paragraph (str): The paragraph of text
            style (str): the style (defaults to roman)

        Returns:
            (int) the number of lines generated
        '''
        # some variables that we will use
        usedline = 0 # how much of the line have we used?
        missing_chars = 0 # how many missing characters did we hit?
        linecounter = 0 # how many lines of tape are we going to use?
        numspaces = 0 # track the number of spaces in a line

        # to make life easier for the person casting the galley we are going to pad each line
        # with four quads (2 at beginning and end), this helps to ensure that the sorts don't fall over
        quad_column, quad_row = self.case.get_char(self.case.QUAD)
        quadwidth = Utils.width(self.case.QUAD, self.case, self.wedge)
        units_of_set_per_line = self.units_of_set_per_line - 4 * quadwidth

        # split the paragraph into words (on the space)
        words = paragraph.strip().split(' ')

        module_logger.debug("Begin Paragraph")
        i=0
        while i < len(words):
            word = words[i]

            # need to ensure that the whole word will fit on the line
            # if there are already words in the line then ensure a space
            # is prepended
            if usedline == 0:
                wordwidth = 0
                # Cast the initial 2 quads
                Utils.draw([str(quad_column),str(quad_row)], self.case.QUAD)
                Utils.draw([str(quad_column),str(quad_row)], self.case.QUAD)
                linecounter += 2
            else:
                wordwidth = self.lowerlimit_space

            wordwidth += Utils.wordwidth(word, self.case, self.wedge, style)

            # can we fit this word (and maybe the space) into the line?
            if usedline + wordwidth < units_of_set_per_line:
                if usedline != 0:
                    column, row = self.case.get_char(' ')
                    Utils.draw(['S',str(column),str(row)]," ","Jspace")
                    linecounter += 1
                    numspaces += 1
                for the_char in word:
                    column, row = self.case.get_char(the_char, style)
                    Utils.draw([str(column),str(row)],the_char)
                    linecounter += 1
                usedline += wordwidth
                # increment word counter
                i += 1

            # what about if we hypenate, can we fit the hypernated word?
            elif Utils.besthyphenation(word,self.case,self.wedge,style,units_of_set_per_line-usedline-self.lowerlimit_space)[0] != "":
                module_logger.debug(f"Space remaining on line {round(units_of_set_per_line-usedline-self.lowerlimit_space)} (picas)")
                module_logger.debug(f"'{word}'' too big ({Utils.wordwidth(word, self.case, self.wedge)} picas)")
                hypenation_options = Utils.besthyphenation(word,self.case,self.wedge,style,units_of_set_per_line-usedline-self.lowerlimit_space)
                wordwidth = Utils.wordwidth(hypenation_options[0], self.case, self.wedge)
                module_logger.debug(f"Using hyphenation: '{hypenation_options[0]}' ({wordwidth} picas) and '{hypenation_options[1]}' ({Utils.wordwidth(hypenation_options[1], self.case, self.wedge)} picas)")
                if usedline != 0:
                    column, row = self.case.get_char(' ')
                    Utils.draw(['S',str(column),str(row)]," ","Jspace")
                    linecounter += 1
                    numspaces += 1
                for the_char in hypenation_options[0]:
                    column, row = self.case.get_char(the_char)
                    Utils.draw([str(column),str(row)],the_char)
                    linecounter += 1
                usedline += wordwidth
                # replace the current word with the hypenation and don't increament the counter
                words[i] = hypenation_options[1]

            # no hyernation options and can't fit, justify the line, put the word on the newline
            else:
                #cast the quads at the end of the line
                Utils.draw([str(quad_column),str(quad_row)], self.case.QUAD)
                Utils.draw([str(quad_column),str(quad_row)], self.case.QUAD)
                
                total_space_remaining = units_of_set_per_line - usedline
                self.justifyspaces(total_space_remaining, numspaces)

                linecounter += 4 # 2 quads and two justification lines
                usedline = 0
                numspaces = 0
                # don't increment the word counter (so the current word
                # will be processed again on the new line)
        
        # we are out of words, so end the paragraph.
        # Only need to do this if the line has words on it
        if usedline != 0:
            module_logger.debug(f"End of paragraph: Padding with quads and j-spaces")
            # need to pad the remaining line with quads and spaces then justify
            charwidth = quadwidth
            while usedline + charwidth + self.lowerlimit_space <= units_of_set_per_line:
                # add as many quads as we can to fill
                Utils.draw([str(quad_column),str(quad_row)], self.case.QUAD, "Padding Quad")
                linecounter += 1
                usedline += charwidth

            while usedline + self.lowerlimit_space <= units_of_set_per_line:
                # add as many justification spaces as we can to fill
                column, row = self.case.get_char(' ')
                Utils.draw(['S',str(column),str(row)], " ", "Padding JSpace")
                linecounter += 1
                usedline += self.lowerlimit_space
                numspaces += 1

            # add two quads at the end
            Utils.draw([str(quad_column),str(quad_row)], self.case.QUAD)
            Utils.draw([str(quad_column),str(quad_row)], self.case.QUAD)
            linecounter += 2

            # now justify
            self.justifyspaces(units_of_set_per_line - usedline, numspaces)
            linecounter += 2

        return linecounter

    # ------------------------------------------------------------
    def seperator_generator(self) -> int:
        '''Generate a justified line of quads

        Returns:
            (int) the number of lines generated
        '''

        linecounter = 0 # how many lines of tape are we going to use?
        usedline = 0 # how much of the line have we used?
        numspaces = 0 # how many spaces have we used?

        # to make life easier for the person casting the galley we are going to pad each line
        # with four quads (2 at beginning and end), this helps to ensure that the sorts don't fall over
        quad_column, quad_row = self.case.get_char(self.case.QUAD)
        quadwidth = Utils.width(self.case.QUAD, self.case, self.wedge)
        units_of_set_per_line = self.units_of_set_per_line - 4 * quadwidth

        # cast the initial padding quads
        Utils.draw([str(quad_column),str(quad_row)], self.case.QUAD)
        Utils.draw([str(quad_column),str(quad_row)], self.case.QUAD)
        linecounter += 2

        charwidth = quadwidth
        while usedline + charwidth + self.lowerlimit_space <= units_of_set_per_line:
            # add as many quads as we can to fill
            Utils.draw([str(quad_column),str(quad_row)], self.case.QUAD, "Seperator Quad")
            linecounter += 1
            usedline += charwidth

        while usedline + self.lowerlimit_space <= units_of_set_per_line:
            # add as many justification spaces as we can to fill
            column, row = self.case.get_char(' ')
            Utils.draw(['S',str(column),str(row)], " ", "Padding JSpace")
            linecounter += 1
            usedline += self.lowerlimit_space
            numspaces += 1

        # add two quads at the end
        Utils.draw([str(quad_column),str(quad_row)], self.case.QUAD)
        Utils.draw([str(quad_column),str(quad_row)], self.case.QUAD)
        linecounter += 2

        # now justify
        self.justifyspaces(units_of_set_per_line - usedline, numspaces)
        linecounter += 2

        return linecounter