import tkinter as tk
from tkinter import filedialog
import os
import sys
from glob import glob
from collections import defaultdict
import operator
from pathlib import Path

# Hide the main tkinter window

root = tk.Tk()
root.withdraw()

count_dict = defaultdict(int)

# Ask user to select input directory
print("Please select the input directory...")
input_dir = filedialog.askdirectory(title="Select input directory")

for path in Path(input_dir).rglob('*.txt'):
    
    with open(path, 'r') as file:
        file_content = file.read()

        values = file_content.split(',')        

            # Iterate over the values
        for value in values:
            # Trim any leading or trailing whitespaces
            value = value.strip()
            
            if("Negative prompt:" in value):
                break
                        
            if value in count_dict:
                count_dict[value] += 1
            else:
                count_dict[value] = 1

# Sort the dictionary by values
sorted_dict = dict(sorted(count_dict.items(), key=operator.itemgetter(1), reverse=True))

file_path = 'C:\\Users\\D13\\Desktop\\output.txt'
with open(file_path, 'w') as file:
    for key, value in sorted_dict.items():
        file.write(key + " : " + str(value) + ", \n")
        #print(key + " : " + str(value))

print(f"Content has been written to {file_path}.")