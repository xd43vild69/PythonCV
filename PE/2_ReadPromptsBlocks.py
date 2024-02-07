import tkinter as tk
from tkinter import filedialog
import os
import sys
from glob import glob
from collections import defaultdict
import operator
from pathlib import Path
from prompt import Prompt

root = tk.Tk()
root.withdraw()
count_dict = defaultdict(int)

prompts = Prompt()

print("Please select the input directory...")
input_dir = filedialog.askdirectory(title="Select input directory")

for path in Path(input_dir).rglob('*.txt'):
    
    with open(path, 'r') as file:
        file_content = file.read()
        values = file_content.split(',')        
        prompts.block = file_content

        for value in values:
            value = value.strip() # Trim leading or trailing whitespaces
            prompts.nextStatus(value)
            prompts.addValue(value)
            print(prompts)
            
            # Add to database t2i
            1. id
            2. img
            3. add metadata

            # Search in database
            1. id
            2. rating
            3. new
            4. repeatition
            5. wModel

            