import customtkinter
import os
import sys
import tkinter as tk
from glob import glob
import cv2
from tkinter import *
from tkinter import filedialog
from pathlib import Path
from distutils.dir_util import copy_tree
import datetime
import uuid
import pathlib
import glob

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("600x500")

def selectInputFiles():
    dir_path = filedialog.askdirectory(title="Select input directory")
    quantity_imgs = countFiles(dir_path) / 2

    if quantity_imgs <= 0:
        print("Empty folder")
        return

    labelTitle.configure(text = f'Lora PP : {os.path.basename(dir_path)}')

    sourceEntry.insert(0,dir_path)    
    quantityFiles.insert(0, quantity_imgs)
    quantityEpochs.insert(0, 1)
    quantityBatchSize.insert(0, 4)
    quantityRepeatition.insert(0, 20)
    totalCalculation = quantity_imgs * 1 * 20 / 4
    quantityTotalTrain.insert(0, totalCalculation)

def recalculate():
    quantityTotalTrain.delete(0, END)
    totalCalculation = float(quantityFiles.get()) * int(quantityEpochs.get()) * int(quantityRepeatition.get()) / int(quantityBatchSize.get())
    quantityTotalTrain.insert(0, totalCalculation)

def countFiles(dir_path):
    count = 0
    for path in os.listdir(dir_path):

        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1
    return count

def cleanFiles():
    sourceEntry.delete(0, END)
    quantityFiles.delete(0, END)
    quantityEpochs.delete(0, END)
    quantityBatchSize.delete(0, END)
    quantityRepeatition.delete(0, END)
    quantityTotalTrain.delete(0, END)
    labelTitle.configure(text = f'Lora PP :')
    return

def createStructure():
    path_dir = Path(sourceEntry.get())
    baseName = os.path.basename(path_dir)

    if not os.path.exists(f'{path_dir.parent.absolute()}\lora_{baseName}'):
        os.makedirs(f'{path_dir.parent.absolute()}\lora_{baseName}')
        os.makedirs(f'{path_dir.parent.absolute()}\lora_{baseName}\image')
        os.makedirs(f'{path_dir.parent.absolute()}\lora_{baseName}\log')
        os.makedirs(f'{path_dir.parent.absolute()}\lora_{baseName}\model')
        os.makedirs(f'{path_dir.parent.absolute()}\lora_{baseName}\image\{quantityRepeatition.get()}_{baseName}')
        copy_tree(sourceEntry.get(), f'{path_dir.parent.absolute()}\lora_{baseName}\image\{quantityRepeatition.get()}_{baseName}')
        createLog(f'{path_dir.parent.absolute()}\lora_{baseName}')
        createConfigJson()

    return

def createLog(path):
            
    file_name = f'{path}\log-{datetime.date.today()}_{uuid.uuid4()}.txt'
    text1 = F'quantity files: {quantityFiles.get()}, quantity epochs: {quantityEpochs.get()}, quantity batch size: {quantityBatchSize.get()}, quantity repeats: {quantityRepeatition.get()}, total calculation: {quantityTotalTrain.get()}'

    with open(file_name, 'w') as file:
        file.write(text1)
    return

def createConfigJson():    
    path_dir = Path(sourceEntry.get())
    basename = os.path.basename(path_dir)

    with open('LoraD13.json', 'r') as file:
        # read a list of lines into data
        data = file.readlines()

    logging_dir = f'  \"logging_dir\":\"{path_dir.parent.absolute()}\\lora_{basename}\\log", '
    output_dir =  f'  \"output_dir\":\"{pathlib.PureWindowsPath(path_dir.parent.absolute())}\\lora_{basename}\\model", '
    train_data_dir =  f'  \"train_data_dir\":\"{pathlib.PurePath(path_dir.parent.absolute())}\\lora_{basename}\\image", '
    output_lora = f'  \"output_name\":\"lora_{basename.replace("_pp", "")}", '
    sample_prompts = f'  \"sample_prompts\":\"{getInitialPrompt()[0]}", '

    data[32] = r"" + logging_dir.replace("\\", "\\\\") + "\n"
    data[59] = r"" + output_dir.replace("\\", "\\\\") + "\n"
    data[86] = r"" + train_data_dir.replace("\\", "\\\\") + "\n"
    data[60] = r"" + output_lora.replace("\\", "\\\\") + "\n"
    data[70] = sample_prompts + "\n"

    if not os.path.exists(f'{path_dir.parent.absolute()}\\lora_{basename}\\lora_config_{basename}.json'):
        with open(f'{path_dir.parent.absolute()}\\lora_{basename}\\lora_config_{basename}.json', 'w') as file:
            file.writelines( data )
    return

def getInitialPrompt():
    path_dir = Path(sourceEntry.get())
    baseName = os.path.basename(path_dir)

    path_init = f'{path_dir.parent.absolute()}\lora_{baseName}\image\{quantityRepeatition.get()}_{baseName}'

    #path = r'E:/demos/files_demos/account/*.txt'
    files = glob.glob(path_init + "\\*.txt")

    print(files)

    data = ""
    with open(files[0], 'r') as file:
        # read a list of lines into data
        data = file.readlines()
    return data

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

labelTitle = customtkinter.CTkLabel(master=frame, text="Lora PP")
labelTitle.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=frame, text="Select Path", command=selectInputFiles)
button.place(x=80, y=80)

sourceEntry = customtkinter.CTkEntry(master=frame, placeholder_text="SourceImgs")
sourceEntry.place(x=240, y=80)

quantityImgs = customtkinter.CTkLabel(master=frame, text="QuantityFiles")
quantityImgs.place(x=80, y=130)

quantityFiles = customtkinter.CTkEntry(master=frame, placeholder_text="QuantityFiles")
quantityFiles.place(x=240, y=130)

repeatition = customtkinter.CTkLabel(master=frame, text="Repets")
repeatition.place(x=80, y=180)

quantityRepeatition = customtkinter.CTkEntry(master=frame, placeholder_text="Repets")
quantityRepeatition.place(x=240, y=180)

epochs = customtkinter.CTkLabel(master=frame, text="Epochs")
epochs.place(x=80, y=230)

quantityEpochs = customtkinter.CTkEntry(master=frame, placeholder_text="Epochs")
quantityEpochs.place(x=240, y=230)

batchSize = customtkinter.CTkLabel(master=frame, text="batchSize")
batchSize.place(x=80, y=280)

quantityBatchSize = customtkinter.CTkEntry(master=frame, placeholder_text="BatchSize")
quantityBatchSize.place(x=240, y=280)

totalTrain = customtkinter.CTkLabel(master=frame, text="totalTrain")
totalTrain.place(x=80, y=330)

quantityTotalTrain = customtkinter.CTkEntry(master=frame, placeholder_text="totalTrain")
quantityTotalTrain.place(x=240, y=330)

buttonRecalculate = customtkinter.CTkButton(master=frame, text="Calculation", command=recalculate)
buttonRecalculate.place(x=80, y=380)

buttonCreateStructure = customtkinter.CTkButton(master=frame, text="Create Structure", command=createStructure)
buttonCreateStructure.place(x=240, y=380)

buttonClean = customtkinter.CTkButton(master=frame, text="Clean", command=cleanFiles)
buttonClean.place(x=80, y=430)

root.mainloop()

###

