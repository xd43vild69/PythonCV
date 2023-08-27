from tkinter import filedialog
from LoraCalculations import LoraCalculations  # Import the ExternalClass from the external_class module

class LoraFileManager:
    
    loraCalculations = LoraCalculations()
    
    def __init__(self):
        return

    def createStructure():
        print("cs")

    def selectInputFiles():
        dir_path = filedialog.askdirectory(title="Select input directory")
        quantity_imgs = LoraCalculations.countFiles(dir_path) / 2

        if quantity_imgs <= 0:
            print("Empty folder")
            return