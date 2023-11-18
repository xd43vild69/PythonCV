import tkinter as tk
import customtkinter
from tkinter import END
from tkinter import filedialog
import os

from LoraCalculations import LoraCalculations  # Import the ExternalClass from the external_class module
from LoraFileManager import LoraFileManager  # Import the ExternalClass from the external_class module

class SimpleUI:

    loraFileManager = LoraFileManager()
            
    def __init__(self, root):
        self.root = root
        self.root.title("Lora UI - Configuration")

        labelTitle = customtkinter.CTkLabel(root, text="Lora PP")
        labelTitle.pack(pady=12, padx=10)

        button = customtkinter.CTkButton(root, text="Select Path", command=self.change_label_text)
        button.place(x=80, y=80)

        sourceEntry = customtkinter.CTkEntry(root, placeholder_text="SourceImgs")
        sourceEntry.place(x=240, y=80)

        quantityImgs = customtkinter.CTkLabel(root, text="QuantityFiles")
        quantityImgs.place(x=80, y=130)

        quantityFiles = customtkinter.CTkEntry(root, placeholder_text="QuantityFiles")
        quantityFiles.place(x=240, y=130)

        repeatition = customtkinter.CTkLabel(root, text="Repets")
        repeatition.place(x=80, y=180)

        quantityRepeatition = customtkinter.CTkEntry(root, placeholder_text="Repets")
        quantityRepeatition.place(x=240, y=180)

        epochs = customtkinter.CTkLabel(root, text="Epochs")
        epochs.place(x=80, y=230)

        quantityEpochs = customtkinter.CTkEntry(root, placeholder_text="Epochs")
        quantityEpochs.place(x=240, y=230)

        batchSize = customtkinter.CTkLabel(root, text="batchSize")
        batchSize.place(x=80, y=280)

        quantityBatchSize = customtkinter.CTkEntry(root, placeholder_text="BatchSize")
        quantityBatchSize.place(x=240, y=280)

        totalTrain = customtkinter.CTkLabel(root, text="totalTrain")
        totalTrain.place(x=80, y=330)

        quantityTotalTrain = customtkinter.CTkEntry(root, placeholder_text="totalTrain")
        quantityTotalTrain.place(x=240, y=330)

        buttonRecalculate = customtkinter.CTkButton(root, text="Calculation", command=self.calculationsLora)
        buttonRecalculate.place(x=80, y=380)

        buttonCreateStructure = customtkinter.CTkButton(root, text="Create Structure", command=self.createStructure)
        buttonCreateStructure.place(x=240, y=380)

        buttonClean = customtkinter.CTkButton(root, text="Clean", command=self.cleanFiles)
        buttonClean.place(x=80, y=430)

    def change_label_text(self):
        print(LoraFileManager.selectInputFiles())

    def createStructure():
        LoraFileManager.createStructure()

    def calculationsLora():
        LoraCalculations.Calculation()

    def cleanFiles(self):
        self.sourceEntry.delete(0, END)
        self.quantityFiles.delete(0, END)
        self.quantityEpochs.delete(0, END)
        self.quantityBatchSize.delete(0, END)
        self.quantityRepeatition.delete(0, END)
        self.quantityTotalTrain.delete(0, END)
        self.labelTitle.configure(text = f'Lora PP :')
        return
    
    def selectInputFiles(self):
        dir_path = filedialog.askdirectory(title="Select input directory")
        quantity_imgs = LoraCalculations.countFolderFiles(dir_path) / 2

        if quantity_imgs <= 0:
            print("Empty folder")
            return

        self.labelTitle.configure(text = f'Lora PP : {os.path.basename(dir_path)}')

        self.sourceEntry.insert(0,dir_path)    
        self.quantityFiles.insert(0, quantity_imgs)
        self.quantityEpochs.insert(0, 1)
        self.quantityBatchSize.insert(0, 4)
        self.quantityRepeatition.insert(0, 20)
        totalCalculation = quantity_imgs * 1 * 20 / 4
        
        self.quantityTotalTrain.insert(0, totalCalculation)
        return    


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root = customtkinter.CTk()
root.geometry("600x500")
ui = SimpleUI(root)
root.mainloop()