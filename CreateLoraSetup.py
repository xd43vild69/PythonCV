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

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("1024x700")

def selectInputFiles():
    #print("Test1")
    dir_path = filedialog.askdirectory(title="Select input directory")
    quantity_imgs = countFiles(dir_path)

    sourceEntry.insert(0,dir_path)    
    quantityFiles.insert(0, quantity_imgs)
    quantityEpochs.insert(0, 1)
    quantityBatchSize.insert(0, 4)
    quantityRepeatition.insert(0, 20)
    totalCalculation = quantity_imgs / 2 * 1 * 20 / 4
    quantityTotalTrain.insert(0, totalCalculation)

def recalculate():
    quantityTotalTrain.delete(0, END)
    totalCalculation = (float(quantityFiles.get()) / 2) * int(quantityEpochs.get()) * int(quantityRepeatition.get()) / int(quantityBatchSize.get())
    quantityTotalTrain.insert(0, totalCalculation)

def countFiles(dir_path):
    count = 0
    for path in os.listdir(dir_path):

        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1
    return count

def createStructure():
    path_dir = Path(sourceEntry.get())
    baseName = os.path.basename(path_dir)

    if not os.path.exists(f'{path_dir.parent.absolute()}\lora_{baseName}'):
        os.makedirs(f'{path_dir.parent.absolute()}\lora_{baseName}')
        os.makedirs(f'{path_dir.parent.absolute()}\lora_{baseName}\image')
        os.makedirs(f'{path_dir.parent.absolute()}\lora_{baseName}\log')
        os.makedirs(f'{path_dir.parent.absolute()}\lora_{baseName}\model')
        os.makedirs(f'{path_dir.parent.absolute()}\lora_{baseName}\image\{quantityRepeatition.get()}_baseName')
        copy_tree(sourceEntry.get(), f'{path_dir.parent.absolute()}\lora_{baseName}\image\{quantityRepeatition.get()}_baseName')
        createLog(f'{path_dir.parent.absolute()}\lora_{baseName}')

    return

def createLog(path):
            
    file_name = f'{path}\log-{datetime.date.today()}_{uuid.uuid4()}.txt'
    text1 = F'quantity files: {quantityFiles.get()}, quantity epochs: {quantityEpochs.get()}, quantity batch size: {quantityBatchSize.get()}, quantity repeats: {quantityRepeatition.get()}, total calculation: {quantityTotalTrain.get()}'

    with open(file_name, 'w') as file:
        file.write(text1)
    return

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Lora PP")
label.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=frame, text="Select Path", command=selectInputFiles)
button.pack(pady=5, padx=10)

sourceEntry = customtkinter.CTkEntry(master=frame, placeholder_text="SourceImgs")
sourceEntry.pack(pady=5, padx=10)

quantityImgs = customtkinter.CTkLabel(master=frame, text="QuantityFiles")
quantityImgs.pack(pady=5, padx=10)

quantityFiles = customtkinter.CTkEntry(master=frame, placeholder_text="Path")
quantityFiles.pack(pady=5, padx=10)

repeatition = customtkinter.CTkLabel(master=frame, text="Repetition")
repeatition.pack(pady=5, padx=10)

quantityRepeatition = customtkinter.CTkEntry(master=frame, placeholder_text="Repetition")
quantityRepeatition.pack(pady=5, padx=10)

epochs = customtkinter.CTkLabel(master=frame, text="Epochs")
epochs.pack(pady=5, padx=10)

quantityEpochs = customtkinter.CTkEntry(master=frame, placeholder_text="Epochs")
quantityEpochs.pack(pady=5, padx=10)

batchSize = customtkinter.CTkLabel(master=frame, text="batchSize")
batchSize.pack(pady=5, padx=10)

quantityBatchSize = customtkinter.CTkEntry(master=frame, placeholder_text="BatchSize")
quantityBatchSize.pack(pady=5, padx=10)

totalTrain = customtkinter.CTkLabel(master=frame, text="totalTrain")
totalTrain.pack(pady=5, padx=10)

quantityTotalTrain = customtkinter.CTkEntry(master=frame, placeholder_text="totalTrain")
quantityTotalTrain.pack(pady=5, padx=10)

buttonRecalculate = customtkinter.CTkButton(master=frame, text="Calculation", command=recalculate)
buttonRecalculate.pack(pady=5, padx=10)

buttonCreateStructure = customtkinter.CTkButton(master=frame, text="Create Structure", command=createStructure)
buttonCreateStructure.pack(pady=5, padx=10)

root.mainloop()

###

