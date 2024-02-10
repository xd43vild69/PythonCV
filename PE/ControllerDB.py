import tkinter as tk
from tkinter import filedialog
import os
import time
import sys
from glob import glob
from collections import defaultdict
import operator
from pathlib import Path
from prompt import Prompt
from dbManager import DBManager

root = tk.Tk()
root.withdraw()
count_dict = defaultdict(int)

print("Please select the input directory...")
input_dir = filedialog.askdirectory(title="Select input directory")

tblName = "tblt2i"

def AddSDt2i():

    for path in Path(input_dir).rglob('*.txt'):
        
        with open(path, 'r') as file:
            prompts = Prompt()
            file_content = file.read()
            file_content = file_content.replace('\n', ',')

            values = file_content.split(',')
            
            prompts.block = file_content

            prompts.currentState = "Positive:"
            prompts.createdDate = time.ctime(os.path.getctime(file.name))
            prompts.filePath = file.name

            try:
                for value in values:
                    value = value.strip() # Trim leading or trailing whitespaces
                    if(value != ''):
                        prompts.nextStatus(value)
                        prompts.addValue(value)
                    else:
                        print("empty")

                dbmng = DBManager()
                dbmng.Addt2i(prompts)

                print("row: {0}", count=+1)      

            except Exception as error:
                print("error: {0}", error)      

def AddSDi2i():
    count = 0
    for path in Path(input_dir).rglob('*.txt'):
        
        with open(path, 'r') as file:
            prompts = Prompt()
            file_content = file.read()
            values = file_content.split(',')

            prompts.block = file_content
            
            prompts.currentState = "Positive:"
            prompts.createdDate = time.ctime(os.path.getctime(file.name))
            prompts.filePath = file.name
            
            try:
                for value in values:
                    pValue = value.split("\n")
                    for v in pValue:
                        v = v.strip() # Trim leading or trailing whitespaces
                        prompts.nextStatus(v)
                        prompts.addValue(v)

                dbmng = DBManager()
                dbmng.Addi2i(prompts)
                count=count+1
                print(count, "row")      
            except Exception as error:
                print("error: {0}", error)                

AddSDi2i()   

