# this is the init UI class

import tkinter
from tkinter import messagebox
import customtkinter
from Normalizer import Normalizer 
import os
import sys
import datetime
import uuid
import glob
from tkinter import filedialog
from pathlib import Path
from distutils.dir_util import copy_tree
import pathlib
import subprocess

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):

    LORA = ""

    def __init__(self):
        super().__init__()

        # configure window
        self.title("Dataset helper")
        self.geometry(f"{600}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)
        
        gpady = 10
        gpadx = 20

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Preparation", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=0, pady=gpady)
        
        self.lora_version = str(self.get_last_lora_version())
        self.lora_name = "xl_Theme_v" + self.lora_version
        self.lora_name_version = ""
        self.normalizer_path = ""
        self.absolute_path = str(self.get_lora_training_folder())

        self.siderbar_loraValue = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text=self.lora_name)
        self.siderbar_loraValue.grid(row=1, column=0, padx=gpadx, pady=gpady)

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Normalizer 1024", command=self.normalizer)
        self.sidebar_button_1.grid(row=2, column=0, padx=gpadx, pady=gpady)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Augmentation", command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=3, column=0, padx=gpadx, pady=gpady)
        #self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Captation", command=self.captationizer)
        #self.sidebar_button_3.grid(row=4, column=0, padx=gpadx, pady=gpady)
        #self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Test", command=self.test_button_event)
        #self.sidebar_button_3.grid(row=5, column=0, padx=gpadx, pady=gpady)        

        # self is the right window place

        self.labelTitle = customtkinter.CTkLabel(self, text="Calculations from source", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.labelTitle.place(x=280, y=10) 

        self.buttonl1 = customtkinter.CTkButton(self, text="Select Path", command=self.selectInputFiles)
        self.buttonl1.place(x=200, y=60)      
        self.sourceEntry = customtkinter.CTkEntry(self, placeholder_text="SourceImgs")
        self.sourceEntry.place(x=360, y=60)

        self.quantityImgs = customtkinter.CTkLabel(self, text="QuantityFiles")
        self.quantityImgs.place(x=200, y=110)
        self.quantityFiles = customtkinter.CTkEntry(self, placeholder_text="QuantityFiles")
        self.quantityFiles.place(x=360, y=110)

        self.repeatition = customtkinter.CTkLabel(self, text="Repets")
        self.repeatition.place(x=200, y=160)
        self.quantityRepeatition = customtkinter.CTkEntry(self, placeholder_text="Repets")
        self.quantityRepeatition.place(x=360, y=160)

        self.epochs = customtkinter.CTkLabel(self, text="Epochs")
        self.epochs.place(x=200, y=210)
        self.quantityEpochs = customtkinter.CTkEntry(self, placeholder_text="Epochs")
        self.quantityEpochs.place(x=360, y=210)

        self.batchSize = customtkinter.CTkLabel(self, text="batchSize")
        self.batchSize.place(x=200, y=260)
        self.quantityBatchSize = customtkinter.CTkEntry(self, placeholder_text="BatchSize")
        self.quantityBatchSize.place(x=360, y=260)

        self.totalTrain = customtkinter.CTkLabel(self, text="totalTrain")
        self.totalTrain.place(x=200, y=310)
        self.quantityTotalTrain = customtkinter.CTkEntry(self, placeholder_text="totalTrain")
        self.quantityTotalTrain.place(x=360, y=310)

        self.buttonRecalculate = customtkinter.CTkButton(self, text="Calculation", command=self.recalculate)
        self.buttonRecalculate.place(x=200, y=360)

        self.buttonCreateStructure = customtkinter.CTkButton(self, text="Create Folder", command=self.createTrainigStructures)
        self.buttonCreateStructure.place(x=360, y=360)

        self.buttonClean = customtkinter.CTkButton(self, text="Clean", command=self.cleanFiles)
        self.buttonClean.place(x=200, y=410)

    def get_last_lora_version(self):
        try:
            with open("LoraCounter.txt", "r") as file:
                lora_version = int(file.read()) + 1
        except FileNotFoundError:
            lora_version = 1
        except ValueError:
            lora_version = 1

        with open("LoraCounter.txt", "w") as file:
            file.write(str(lora_version))

        return lora_version
    
    def get_lora_training_folder(self):
        try:
            with open("LoraCTrainingFolder.txt", "r") as file:
                lora_training_folder = file.read().strip()  # Use strip() to remove any extra whitespace or newlines
        except FileNotFoundError:
            print("LoraCTrainingFolder.txt not found.")
            lora_training_folder = ""
        except Exception as e:
            print(f"An error occurred: {e}")
            lora_training_folder = ""

        return lora_training_folder

    def sidebar_button_event(self):
        print("sidebar_button click")

    def test_button_event(self):
        messagebox.showinfo("x")

    def finish_button_event(self):
        messagebox.showinfo("Complete", "Done")

    def normalizer(self):
        if not self.validationName():
            print("Please select the source directory...")
            return  # Exit early if validation fails

        input_dir = filedialog.askdirectory(title="Select source directory")
        
        if not input_dir:  # Handle case where user cancels directory selection
            print("No directory selected. Operation canceled.")
            return

        self.normalizer_path = input_dir + '_N'

        # If output directory does not exist, create it
        if not os.path.exists(self.normalizer_path):
            os.makedirs(self.normalizer_path)
        
        try:
            Normalizer(input_dir, self.normalizer_path)
        except Exception as e:
            print(f"An error occurred during normalization: {e}")
            return

        self.finish_button_event()
    
    def captationizer(self):
        if not self.normalizer_path:
            messagebox.showinfo("Error", "There is no folder to process.")
            return  # Exit early if there is no folder to process

        path_joy_captation = 'C:\\dev\\joy_caption\\joy-caption-pre-alpha\\app.py'
        
        try:
            # Use subprocess.run for better exception handling
            subprocess.run(["python", path_joy_captation, self.normalizer_path], check=True)
            print("Captation Finished")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Captation process failed: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
    
    def open_input_dialog_normalize_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type lora name:", title="Normalizer")
        user_input = dialog.get_input()
    
        if user_input:  # Check if input is not empty or None
            print("Normalizer:", user_input)
        else:
            print("No input provided.")

        print("Normalizer:", dialog.get_input())

    def selectInputFiles(self):

        self.cleanFiles()  # Clear any existing values in the entry fields

        if not self.validationName():  # Validate first
            return  # Exit early if validation fails

        self.LORA = self.lora_name_version  # Set LORA variable

        # Prompt the user to select an input directory
        dir_path = filedialog.askdirectory(title="Select input directory")

        if not dir_path:  # Handle case where the user cancels the directory selection
            print("No directory selected. Operation canceled.")
            return

        # Count the number of files (assuming every image has a corresponding pair, hence divided by 2)
        quantity_imgs = self.countFiles(dir_path) / 2

        if quantity_imgs <= 0:  # If the folder is empty, exit early
            print("Empty folder")
            return

        # Update the UI with the selected source directory
        self.labelTitle.configure(text=f'Source: {os.path.basename(dir_path)}')
    
        # Insert the new values into the respective input fields
        self.sourceEntry.insert(0, dir_path)
        self.quantityFiles.insert(0, quantity_imgs)

        # Default values for epochs, batch size, and repetitions
        default_epochs = 1
        default_batch_size = 1
        default_repetitions = 20

        self.quantityEpochs.insert(0, default_epochs)
        self.quantityBatchSize.insert(0, default_batch_size)
        self.quantityRepeatition.insert(0, default_repetitions)

        # Calculate the total training steps
        totalCalculation = (quantity_imgs * default_epochs * default_repetitions) / 2
        self.quantityTotalTrain.insert(0, totalCalculation)

        return

    def countFiles(self, dir_path):
        count = 0
        for path in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, path)):
                count += 1
        return count
    
    def recalculate(self):
        try:
            # Clear the total quantity entry
            self.quantityTotalTrain.delete(0, tkinter.END)
            
            # Retrieve and validate input values
            quantity_files = float(self.quantityFiles.get())
            quantity_epochs = int(self.quantityEpochs.get())
            quantity_repeats = int(self.quantityRepeatition.get())
            quantity_batch_size = int(self.quantityBatchSize.get())
            
            # Check for division by zero
            if quantity_batch_size == 0:
                messagebox.showinfo("Error", "Batch size cannot be zero.")
                return
            
            # Calculate total training quantity
            self.totalCalculation = quantity_files * quantity_epochs * quantity_repeats / quantity_batch_size
            
            # Update the total quantity entry
            self.quantityTotalTrain.insert(0, self.totalCalculation)
            
        except ValueError:
            messagebox.showinfo("Error", "Please enter valid numbers in all fields.")
        except Exception as e:
            messagebox.showinfo("Error", str(e))

        return

    def cleanFiles(self):
        self.sourceEntry.delete(0, tkinter.END)
        self.quantityFiles.delete(0, tkinter.END)
        self.quantityEpochs.delete(0, tkinter.END)
        self.quantityBatchSize.delete(0, tkinter.END)
        self.quantityRepeatition.delete(0, tkinter.END)
        self.quantityTotalTrain.delete(0, tkinter.END)
        self.labelTitle.configure(text = f'Lora Helper :')
        return
    
    def createTrainigStructures(self):
        self.createStructure()
        self.finish_button_event()

    def createStructure(self):
        try:
            path_dir = Path(self.sourceEntry.get())
            base_name = path_dir.name

            # Base directory for the Lora model
            lora_base_path = Path(self.absolute_path) / f'{self.lora_version}_lora_{self.LORA}'

            # List of subdirectories to create
            subdirs = [
                'image',
                'log',
                'model_15',
                'model_xl',
                'model_flux',
                f'image/{self.quantityRepeatition.get()}_{self.LORA}'
            ]

            # Create base directory if it doesn't exist
            if not lora_base_path.exists():
                lora_base_path.mkdir(parents=True)

                # Create subdirectories
                for subdir in subdirs:
                    (lora_base_path / subdir).mkdir(parents=True)

                # Copy source files to the new image directory
                copy_tree(str(path_dir), str(lora_base_path / f'image/{self.quantityRepeatition.get()}_{self.LORA}'))

                # Create log and configuration files
                self.createLog(str(lora_base_path))
                self.createConfigJson()
                self.createConfigJsonXL()
                self.createConfigJsonFlux()
                self.setKeywordLora()
            else:
                print("Folder already exists")
        except Exception as e:
            messagebox.showinfo("Error", str(e))

        return

    def createLog(self, path):
        # Generate a unique filename for the log
        file_name = os.path.join(path, f'log-{datetime.date.today()}_{uuid.uuid4()}.txt')

        # Create a log message with configuration details
        log_message = (
            f'Quantity files: {self.quantityFiles.get()}, '
            f'Quantity epochs: {self.quantityEpochs.get()}, '
            f'Quantity batch size: {self.quantityBatchSize.get()}, '
            f'Quantity repeats: {self.quantityRepeatition.get()}, '
            f'Total calculation: {self.quantityTotalTrain.get()}'
        )

        try:
            # Write the log message to the file
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(log_message)
        except Exception as e:
            print(f"Error creating log file: {e}")

        return

    def createConfigJson(self):    
        path_dir = Path(self.sourceEntry.get())

        with open('LoraD13.json', 'r') as file:
            # read a list of lines into data
            data = file.readlines()

        output_dir =  f'  \"output_dir\":\"{pathlib.PureWindowsPath(self.absolute_path)}\\{self.lora_version}_lora_{self.LORA}\\model_15", '
        train_data_dir =  f'  \"train_data_dir\":\"{pathlib.PurePath(self.absolute_path)}\\{self.lora_version}_lora_{self.LORA}\\image", '
        output_lora = f'  \"output_name\":\"{self.LORA}", '
        sample_prompts = f'  \"sample_prompts\":\"{self.getInitialPrompt()}", '

        data[59] = r"" + output_dir.replace("\\", "\/") + "\n"
        data[60] = r"" + output_lora.replace("\\", "\/") + "\n"
        data[70] = r"" + train_data_dir.replace("\\", "\/") + "\n"        
        data[86] = sample_prompts + "\n"

        if not os.path.exists(f'{self.absolute_path}\\{self.lora_version}_lora_{self.LORA}\\lora_config_{self.LORA}_15.json'):
            with open(f'{self.absolute_path}\\{self.lora_version}_lora_{self.LORA}\\lora_config_{self.LORA}_15.json', 'w') as file:
                file.writelines( data )
        return
    
    def createConfigJsonFlux(self):    
        path_dir = Path(self.sourceEntry.get())

        with open('LoraD13_Flux.json', 'r') as file:
            # read a list of lines into data
            data = file.readlines()

        output_dir =  f'  \"output_dir\":\"{pathlib.PureWindowsPath(self.absolute_path)}\\{self.lora_version}_lora_{self.LORA}\\model_flux", '
        train_data_dir =  f'  \"train_data_dir\":\"{pathlib.PurePath(self.absolute_path)}\\{self.lora_version}_lora_{self.LORA}\\image", '
        output_lora = f'  \"output_name\":\"{self.LORA}", '
        sample_prompts = f'  \"sample_prompts\":\"{self.getInitialPrompt()}", '

        #data[61] = r"" + logging_dir.replace("\\", "\/") + "\n"
        data[122] = r"" + output_dir.replace("\\", "\/") + "\n"
        data[123] = r"" + output_lora.replace("\\", "\/") + "\n"
        data[165] = r"" + train_data_dir.replace("\\", "\/") + "\n"        
        data[136] = sample_prompts + "\n"

        if not os.path.exists(f'{self.absolute_path}\\{self.lora_version}_lora_{self.LORA}\\lora_config_{self.LORA}_flux.json'):
            with open(f'{self.absolute_path}\\{self.lora_version}_lora_{self.LORA}\\lora_config_{self.LORA}_flux.json', 'w') as file:
                file.writelines( data )
        return

    def createConfigJsonXL(self):    
        path_dir = Path(self.sourceEntry.get())

        with open('LoraD13_XL.json', 'r') as file:
            # read a list of lines into data
            data = file.readlines()

        logging_dir = f'  \"logging_dir\":\"{self.absolute_path}\\{self.lora_version}_lora_{self.LORA}\\log", '
        output_dir =  f'  \"output_dir\":\"{pathlib.PureWindowsPath(self.absolute_path)}\\{self.lora_version}_lora_{self.LORA}\\model_xl", '
        train_data_dir =  f'  \"train_data_dir\":\"{pathlib.PurePath(self.absolute_path)}\\{self.lora_version}_lora_{self.LORA}\\image", '
        output_lora = f'  \"output_name\":\"{self.LORA}", '
        sample_prompts = f'  \"sample_prompts\":\"{self.getInitialPrompt()}", '

        data[61] = r"" + logging_dir.replace("\\", "\/") + "\n"
        data[104] = r"" + output_dir.replace("\\", "\/") + "\n"
        data[105] = r"" + output_lora.replace("\\", "\/") + "\n"
        data[140] = r"" + train_data_dir.replace("\\", "\/") + "\n"        
        data[118] = sample_prompts + "\n"

        if not os.path.exists(f'{self.absolute_path}\\{self.lora_version}_lora_{self.LORA}\\lora_config_{self.LORA}_xl.json'):
            with open(f'{self.absolute_path}\\{self.lora_version}_lora_{self.LORA}\\lora_config_{self.LORA}_xl.json', 'w') as file:
                file.writelines( data )
        return

    def setKeywordLora(self):
        path_dir = Path(self.sourceEntry.get())

        path_init = f'{self.absolute_path}\{self.lora_version}_lora_{self.LORA}\image\{self.quantityRepeatition.get()}_{self.LORA}'

        files = glob.glob(path_init + "\\*.txt")
        data = ""
        for file in files:
            try:
                with open(file, 'r') as f:
                    data = f.readlines()
                dataAlteration = self.LORA + ", " + data[0]
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(dataAlteration)
            except:
                print("Keyword exception on file")

        return           

    def getInitialPrompt(self):
        # Get the directory path from the sourceEntry
        path_dir = Path(self.sourceEntry.get())
        
        # Construct the path to the target text files
        path_init = os.path.join(self.absolute_path, f'{self.lora_version}_lora_{self.LORA}', 'image', f'{self.quantityRepeatition.get()}_{self.LORA}')
        
        # Get all .txt files from the constructed path
        files = glob.glob(os.path.join(path_init, "*.txt"))

        # Check if any files were found
        if not files:
            print("No text files found in the directory.")
            return None

        # Read the first line of the first .txt file found
        data = ""
        try:
            with open(files[0], 'r') as file:
                data = file.readline().strip()  # Use strip() to remove line breaks
        except Exception as e:
            print(f"Error reading file: {e}")
            return None

        return data    
    
    def validationName(self):
        if (self.siderbar_loraValue == ""):
            print("No lora name defined")
            return False
        else:

            try:
                new_name = self.siderbar_loraValue + "_v" + self.lora_version
                self.lora_name_version = new_name
            except:
                new_name = self.siderbar_loraValue.get() + "_v" + self.lora_version  
                self.lora_name_version = new_name                              
            
            return True

if __name__ == "__main__":
    app = App()
    app.mainloop()