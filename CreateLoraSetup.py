import customtkinter
import os
import sys
import tkinter as tk
from glob import glob
import cv2
from tkinter import *
from tkinter import filedialog

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

    totalCalculation = (quantity_imgs / 2) * 1 * 4 * 20

    quantityTotalTrain.insert(0, totalCalculation)


def recalculate():
    quantityTotalTrain.delete(0, END)
    totalCalculation = (float(quantityFiles.get()) / 2) * int(quantityEpochs.get()) * int(quantityBatchSize.get()) * int(quantityRepeatition.get())
    quantityTotalTrain.insert(0, totalCalculation)

def countFiles(dir_path):
    count = 0
    for path in os.listdir(dir_path):

        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1
    return count

def set_text(text):
    #entry2.delete(0,END)
    sourceEntry.insert(0,text)
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

root.mainloop()

###

