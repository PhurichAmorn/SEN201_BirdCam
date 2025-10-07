'''
upload.py

This module help import the pseudocode file into a string

Author: Phurich Amornnara (Phu)
Date: 03/10/2025
'''

import os

class FileLoader:
    """
    Load the file that user want to convert to flowchart
    """
    def __init__(self):
        self.filepath = None # store the filepath
        self.content = "" # store the pseudocode

    """
    read a pseudocode .psc file
    Arg:
        filepath - path of the pseudocode file (.psc)
    Return:
        string of the pseudocode
    """
    def load_file(self, path: str) -> str:
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        if not path.lower().endswith(".psc"):
            raise ValueError(f"Invalid file type: {path}. Only '.psc' files are allowed.")

        self.filepath = path  # save the filepath
        with open(path, "r", encoding="utf-8") as f:
            self.content = f.read()

        return self.content

if __name__ == "__main__":
    # Test the file loader
    example_filepath = "../pseudo_example.psc"

    loader = FileLoader()
    code = loader.load_file(example_filepath)

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
