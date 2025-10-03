'''
import.py

This module help import the pseudocode file into a string

Author: Phurich Amornnara (Phu)
Date: 3 October 2025

'''

import os

class FileLoader:
    def __init__(self):
        self.filepath = None # store the filepath
        self.content = "" # store the pseudocode

    """
    read a pseudocode .txt file
    Arg:
        filepath - path of the pseudocode file
    Return:
        string of the pseudocode
    """
    def load_file(self, filepath: str) -> str:
        
        if not os.path.exists(filepath): # if file cannot be find
            raise FileNotFoundError(f"File not found: {filepath}")

        self.filepath = filepath # save the filepath
        with open(filepath, "r") as f:
            self.content = f.read()

        return self.content

if __name__ == "__main__":
    # Test the file loader
    filepath = "../pseudo_example.txt"

    loader = FileLoader()
    code = loader.load_file(filepath)

    print(code)


# Output
'''
--------------------------------------------------
set total_items = 0
set total_vat = 0
set grand_total = 0
for item in item_set
    set vat = 0
    if item_price >= 100
        Set vat = item_price * 0.07
    endif
    print "Name: {item_name} Price: {item_price} VAT: {vat} Price+VAT: {item_price + vat}"
    set total_items = total_items + item_price
    set total_vat = total_vat + vat
    set grand_total = grand_total + item_price + vat
endfor
print "Number of item: {total_items}, VAT: {total_vat}฿, Total: {grand_total}฿"
--------------------------------------------------
'''