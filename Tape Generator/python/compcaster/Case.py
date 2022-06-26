'''
The classes concerning the Matrix Case
'''
from typing import TextIO, List, Tuple
import logging
import unicodedata
import re

# create logger
module_logger = logging.getLogger('compcaster.Case')

# -------------------------------------------------------------------------------
class Matrix:
    '''
    Matrix holds an individual character and character style
    '''
    def __init__(self, the_char: str, the_style: str = None, unitshift: bool = False) -> None:
        self.logger = logging.getLogger('compcaster.Case.Matrix')
        self.the_char = the_char
        self.the_style = the_style
        self.unitshift = unitshift

# -------------------------------------------------------------------------------
class MatrixRow:
    '''
    Holds a row of Matrix in the MatrixCase
    '''

    def __init__(self, matrixcolumndata: List = None) -> None:
        self.logger = logging.getLogger('compcaster.Case.MatrixRow')
        self.matrixcontent = []
        self.iteratorindex = 0
        if matrixcolumndata is not None:
            self.add_row(matrixcolumndata)

    # ----------------------
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.iteratorindex < len(self.matrixcontent):
            self.iteratorindex += 1
            return self.matrixcontent[self.iteratorindex-1]
        else:
            self.iteratorindex = 0
            raise StopIteration

    # ----------------------
    def addelement(self, matrixelement: Matrix) -> None:
        '''Add a ekement to the matrix'''
        self.matrixcontent.append(matrixelement)

    # ----------------------
    def updateelement(self, column: int, the_char: str, the_style: str = None,) -> None:
        '''Change an element in row. Note: column starts at zero'''
        if self.width() > column:
            self.matrixcontent[column].the_char = the_char
            self.matrixcontent[column].the_style = the_style
            self.logger.debug(f"Updated Col:{column} with {the_char} {the_style}")
        else:
            self.logger.error(f"Can't update column {column} as exceeds column count of {self.width()}")

    # ----------------------
    def logRow(self) -> None:
        '''Print the content to the logger'''
        contentstring = ""
        for matrix in self.matrixcontent:
            contentstring += f"{matrix.the_char}-{matrix.the_style} || "
        self.logger.debug(f"{contentstring}")

    # ----------------------
    def get_char(self, the_char_to_find: str, the_style_to_find: str = None) -> int:
        '''
        Search the Matrix case for the character and style.

        Parameters:
                the_char_to_find (str): the character to search for.
                the_style (str): the style to search for.

        Returns:
                Column (int), Unitshift (bool)
        '''

        for i,column in enumerate(self.matrixcontent):
            if column.the_char == the_char_to_find and column.the_style == the_style_to_find:
                    return i, column.unitshift
        return None, None

    # ----------------------
    def add_row(self, multiplecolumns: List) -> None:
        ''' Add a row of data to the MatrixRow'''
        for column in multiplecolumns:
            
            if unicodedata.normalize('NFC',column) == '..':
                # Skip the double dots
                element = Matrix(None,None)
            elif len(unicodedata.normalize('NFC',column)) == 2:
                element = Matrix(unicodedata.normalize('NFC',column)[0],unicodedata.normalize('NFC',column)[1])
            elif len(unicodedata.normalize('NFC',column)) == 1:
                element = Matrix(unicodedata.normalize('NFC',column)[0])
            else:
                element = Matrix(None,None)
                self.logger.error(f"Wrong Character found in MatrixRow: {column}. Inserting blank.")
            self.addelement(element)

    # ----------------------
    def width(self) -> int:
        '''Return the width of the case'''
        return len(self.matrixcontent)


# -------------------------------------------------------------------------------
class MatrixCase:
    '''
    Matrix Case holds a case layout. You have to pass it a file indicating the
    file containing the layout in the constructor.
    '''
    MATRIX_COLUMNS_15x15 = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O']
    MATRIX_COLUMNS_15x17 = ['NI','NL','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O']
    MATRIX_COLUMNS_16x17 = ['NI','NL','A','B','C','EF','E','F','G','H','I','J','K','L','M','N','O']

    JSPACE = '¤'
    EM_QUAD = '▌'
    QUAD = '█'

    def __init__(self, caselayout_file: str) -> None:
        self.logger = logging.getLogger('compcaster.Case.MatrixCase')
        self.logger.info(f'creating an instance of MatrixCase ({caselayout_file})')
        self.caserows = []

        self.caselayout = caselayout_file
        
        with open(caselayout_file, "r") as f:
            self.parse_caselayout(f)

        self.validate_case()
        self.logCase()

    # ----------------------
    def cast_to_int(self, the_text: str):
        '''Convert a string to a int. Return None if conversion fails'''
        try:
            return int(the_text)
        except ValueError:
            return None

    # ----------------------
    def split_into_rows_column(self, the_text: str) -> List:
        '''Take a string composed of letters and numbers and split on bountry'''
        # https://stackoverflow.com/questions/430079/how-to-split-strings-into-text-and-number
        match = re.match(r"([A-Z]+)([0-9]+)", the_text, re.I)
        if match:
            return match.groups()
    
    # ----------------------
    def case_width(self) -> int:
        '''Return the width of the case'''
        if self.case_height() > 0:
            return self.caserows[0].width()
        else:
            return 0

    # ----------------------
    def case_height(self) -> int:
        '''Return the height of the case'''
        return len(self.caserows)

    # ----------------------
    def case_type(self) -> str:
        '''Return the case type'''
        if self.case_width() == 17 and self.case_height() == 15:
            return self.MATRIX_COLUMNS_15x17
        elif self.case_width() == 17 and self.case_height() == 16:
            return self.MATRIX_COLUMNS_16x17
        elif self.case_width() == 15 and self.case_height() == 15:
            return self.MATRIX_COLUMNS_15x15
        else:
            self.logger.error(f"case_type = Invalid MatrixCaseLayout")
            return None

    # ----------------------
    def parse_caselayout(self, caselayout_file: TextIO) -> bool:
        '''
        Parses a case layout file.

        Parameters:
            caselayout_file (TextIO) : The file to be parsed

        Returns:
            True if parsing successful
            False if parsing unsuccessful
        '''

        for line in caselayout_file:
            # self.logger.debug(f"Parsing - {line}")
            # skip lines that begin with a # or a space or don't contain any data
            if line[0] == "#" or line[0] == " " or len(line) <= 1:
                self.logger.debug(f"Skipping - {line}.")
                pass
            else:
                line_elements = line.split()
                first_object = line_elements[0]

                case_row_number = self.cast_to_int(first_object)

                self.logger.debug(f"Processing - {line_elements}")

                # See if the line starts with a number
                if case_row_number is not None:
                    matrix_row = MatrixRow(line_elements[1:])

                    if self.case_width() == 0 or matrix_row.width() == self.case_width():
                        self.caserows.append(matrix_row)
                    else:
                        self.logger.error(f"Error parsing. Row {first_object} contains {len(line_elements)-1} objects but case should only contain {self.case_width()}")
                        return False
                else:
                    if first_object != "_":
                        # Update the table with the ligatures
                        column_row = self.split_into_rows_column(first_object)
                        # Column_row now looks like ['C','15']
                        try:
                            columnindex = self.case_type().index(column_row[0])
                            #columnindex now contains the column number based on the case type
                            if len(line_elements) == 3:
                                self.update_element(int(column_row[1])-1,columnindex,line_elements[1],line_elements[2])
                                # need to -1 as lists start with zero
                            else:
                                self.update_element(int(column_row[1])-1,columnindex,line_elements[1])
                        except ValueError:
                            pass
                    
                    elif first_object == "_":
                        # Unit Shift Data
                        column_row = self.split_into_rows_column(line_elements[1])
                        try:
                            columnindex = self.case_type().index(column_row[0])
                            self.caserows[int(column_row[1])-1].matrixcontent[columnindex].unitshift = True
                        except ValueError:
                            pass


    # ----------------------
    def get_char(self, the_char_to_find: str, the_style_to_find: str = None) -> Tuple:
        '''
        Search the Matrix case for the character and style.

        You can pass in the row/column reference as the_char_to_find, in which case
        it won't actually search, it will just split and return

        Parameters:
                the_char_to_find (str): the character to search for.
                the_style (str): the style to search for.

        Returns:
                Tuple of Column (alphabetical) and Row (numerical)
        '''
        # Check if the character is a space
        if the_char_to_find == ' ':
            the_char_to_find = self.JSPACE

        for i,row in enumerate(self.caserows):
            found_item, unit_shift = row.get_char(the_char_to_find,the_style_to_find)
            if found_item is not None:
                if unit_shift:
                    # If shifted then add on the D and don't add 1 to i (in effect row-1)
                    return self.case_type()[found_item]+'D', i
                else:
                    return self.case_type()[found_item], i+1
        
        # Check that a row and column were not supplied
        # eg A5, in which case return 'A', 5
        match = re.match(r"([a-z]+)([0-9]+)", the_char_to_find, re.I)
        if match:
            return str(match.group(1)), int(match.group(2))

        self.logger.error(f"Character: {the_char_to_find} Style: {the_style_to_find} was not found")
        return None, None

    # ----------------------
    def list_styles(self) -> List:
        '''
        List all the available styles in the Matrix Case
        '''
        styles = set()
        for row in self.caserows:
            for column in row:
                styles.add(column.the_style)
        self.logger.debug(f"Styles Available: {styles}")
        return list(styles)

    # ----------------------
    def validate_case(self) -> None:
        '''
        Quick check of the case layout. Assume there should be a A-Z and a a-z in all of the available styles
        '''
        # Not exactly an optimal way to do this as loops multiple times, but it is only run once and
        # computers are fast :-)

        if self.case_type() is not None:
            styles = self.list_styles()
            alphabet_u = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
            alphabet_l = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
            for style in styles:
                ab = alphabet_l + alphabet_u
                # now we subtract the characters
                for row in self.caserows:
                    for column in row:
                        if column.the_style == style:
                            try:
                                ab.remove(column.the_char)
                            except ValueError:
                                pass
                if len(ab) != 0:
                    self.logger.warn(f"Missing Characters: {ab} in Style {style}")
        else:
            self.logger.error(f"The case is invalid")
            exit()

    # ----------------------
    def logCase(self) -> None:
        '''Log the case layout'''
        for row in self.caserows:
            row.logRow()

    # -----------------------
    def update_element(self, row: int, column: int, the_char: str, the_style: str = None) -> None:
        '''Update an element and set it to a ligature'''
        try:
            self.caserows[row].updateelement(column,the_char,the_style)
            # self.caserows[row].matrixcontent[column].the_char = the_char
            # self.caserows[row].matrixcontent[column].the_style = the_style
            # self.caserows[row].matrixcontent[column].ligature = True
        except:
            self.logger.error(f"Could not update Row:{row} Col:{column} with {the_char}.")