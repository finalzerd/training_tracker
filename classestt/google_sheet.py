__author__ = "noahpro"
__contact__ = "noah.provenzano@fischerjordan.com"
__version__ = "2021-1-13"

from math import floor
import string
from typing import List
import gspread

class GoogleSheet:
    def __init__(self, file_name:str, sheet_name:str) -> None:
        self.sa = gspread.service_account(filename=r"bin\service_account.json")
        self.file = self.sa.open(file_name)
        self.sheet = self.file.worksheet(sheet_name)

        self.letters_list = list(string.ascii_uppercase)

    def col_string(self, column_int:int) -> str:
        start_index = 1
        return_string = ''
        while column_int > 25 + start_index:
            return_string += chr(65 + int((column_int-start_index)/26) - 1)
            column_int = column_int - (int((column_int-start_index)/26))*26
        return_string += chr(65 - start_index + (int(column_int)))
        return return_string

    def write_list(self, row:int, column:int, list_entry:List[str], vertical:bool=False, user_entered:bool=True) -> None:
        """ Writes a python list to a google sheet one cell per item. """
        if vertical:
            cell_list = self.sheet.range(self.letter_range(row, column, 0, len(list_entry)))
        else:
            cell_list = self.sheet.range(self.letter_range(row, column, len(list_entry), 0))
        
        for i, val in enumerate(list_entry):
            cell_list[i].value = str(val)    
        if user_entered:
            self.sheet.update_cells(cell_list, value_input_option='USER_ENTERED')
        else:
            self.sheet.update_cells(cell_list)

    def letter_range(self, row:int, column:int, width:int, height:int) -> str:
        return f"{self.col_string(column)}{row}:{self.col_string(column + width)}{row + height}"

    def col_search(self, column_header_name:str, row:int=1)-> int:
        column_headers = self.sheet.row_values(row)
        for i, column_header in enumerate(column_headers):
            if column_header == column_header_name:
                return i + 1
        raise ValueError(f"Couldn't find column: {column_header_name}")

    def get_column(self, column_header_name:str) -> List[str]:
        """gets column as list excluding header on row 1"""
        return self.sheet.col_values(self.col_search(column_header_name))[1:]
    
    def get_next_available_row(self, search_col:int=1) -> int:
        """Gets the number of next available row """
        str_list = list(filter(None, self.sheet.col_values(search_col)))
        return len(str_list)+1
    
    def get_next_available_column(self, search_row:int=1) -> int:
        """Gets the number of next available column """
        try:
            str_list = list(filter(None, self.sheet.row_values(search_row)))
        except:
            str_list = []
        return len(str_list)+1
