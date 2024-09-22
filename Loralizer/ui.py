import tkinter
from tkinter import messagebox
import customtkinter
from normalizer import Normalizer
from file_utils import FileUtils
from lora_utils import LoraUtils
import os
from tkinter import filedialog
from lora import Lora

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        self.title("Dataset helper")
        self.geometry(f"{600}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(
            self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        gpady = 10
        gpadx = 20

        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Preparation", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=0, pady=gpady)

        self.lora_version = str(FileUtils.get_last_lora_version())
        self.lora_name = "model" + self.lora_version
        self.lora_name_version = ""
        self.normalizer_path = ""
        self.path = str(FileUtils.get_lora_training_folder())

        self.siderbar_loraValue = customtkinter.CTkEntry(
            self.sidebar_frame, placeholder_text=self.lora_name)
        self.siderbar_loraValue.grid(row=1, column=0, padx=gpadx, pady=gpady)

        self.sidebar_button_1 = customtkinter.CTkButton(
            self.sidebar_frame, text="Normalizer 1024", command=self.normalizer)
        self.sidebar_button_1.grid(row=2, column=0, padx=gpadx, pady=gpady)
        self.sidebar_button_2 = customtkinter.CTkButton(
            self.sidebar_frame, text="Augmentation", command=self.normalizer)
        self.sidebar_button_2.grid(row=3, column=0, padx=gpadx, pady=gpady)
        # self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Captation", command=self.captationizer)
        # self.sidebar_button_3.grid(row=4, column=0, padx=gpadx, pady=gpady)
        # self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Test", command=self.test_button_event)
        # self.sidebar_button_3.grid(row=5, column=0, padx=gpadx, pady=gpady)

        # self is the right window place

        self.labelTitle = customtkinter.CTkLabel(
            self, text="steps from source", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.labelTitle.place(x=280, y=10)

        self.buttonl1 = customtkinter.CTkButton(
            self, text="source", command=self.select_source_files)
        self.buttonl1.place(x=200, y=60)
        self.source = customtkinter.CTkEntry(
            self, placeholder_text="path")
        self.source.place(x=360, y=60)

        self.quantityImgs = customtkinter.CTkLabel(self, text="total files")
        self.quantityImgs.place(x=200, y=110)
        self.total_files = customtkinter.CTkEntry(
            self, placeholder_text="total files")
        self.total_files.place(x=360, y=110)

        self.repeatition = customtkinter.CTkLabel(self, text="repeats")
        self.repeatition.place(x=200, y=160)
        self.total_repeats = customtkinter.CTkEntry(
            self, placeholder_text="repeats")
        self.total_repeats.place(x=360, y=160)

        self.epochs = customtkinter.CTkLabel(self, text="epochs")
        self.epochs.place(x=200, y=210)
        self.total_epochs = customtkinter.CTkEntry(
            self, placeholder_text="epocs")
        self.total_epochs.place(x=360, y=210)

        self.batchSize = customtkinter.CTkLabel(self, text="batch")
        self.batchSize.place(x=200, y=260)
        self.total_batch = customtkinter.CTkEntry(
            self, placeholder_text="batch")
        self.total_batch.place(x=360, y=260)

        self.totalTrain = customtkinter.CTkLabel(self, text="steps")
        self.totalTrain.place(x=200, y=310)
        self.total_steps = customtkinter.CTkEntry(
            self, placeholder_text="steps")
        self.total_steps.place(x=360, y=310)

        self.buttonRecalculate = customtkinter.CTkButton(
            self, text="calculation", command=self.recalculate)
        self.buttonRecalculate.place(x=200, y=360)

        self.buttonCreateStructure = customtkinter.CTkButton(
            self, text="ok", command=self.create_training_structures)
        self.buttonCreateStructure.place(x=360, y=360)

        self.buttonClean = customtkinter.CTkButton(
            self, text="clean", command=self.clean_data)
        self.buttonClean.place(x=200, y=410)

    def init_sidebar(self):
        # Sidebar configuration here
        pass

    def init_main_window(self):
        # Main window widgets configuration here
        pass

    def normalizer(self):
        # if not self.lora_utils.validationName(self):
        #    return

        input_dir = filedialog.askdirectory(title="Select source directory")
        if not input_dir:
            return

        self.normalizer_path = input_dir + '_N'
        if not os.path.exists(self.normalizer_path):
            os.makedirs(self.normalizer_path)

        try:
            Normalizer(input_dir, self.normalizer_path)
        except Exception as e:
            print(f"An error occurred during normalization: {e}")
            return

        messagebox.showinfo("Complete", "Normalization done")

    def recalculate(self):
        try:
            # Clear the total quantity entry
            self.total_steps.delete(0, tkinter.END)

            # Retrieve and validate input values
            quantity_files = float(self.total_files.get())
            quantity_epochs = int(self.total_epochs.get())
            quantity_repeats = int(self.total_repeats.get())
            quantity_batch_size = int(self.total_batch.get())

            # Check for division by zero
            if quantity_batch_size == 0:
                messagebox.showinfo("Error", "Batch size cannot be zero.")
                return

            # Calculate total training quantity
            total_steps = int(quantity_files * \
                quantity_epochs * quantity_repeats / quantity_batch_size)

            # Update the total quantity entry
            self.total_steps.insert(0, total_steps)

        except ValueError:
            messagebox.showinfo(
                "Error", "Please enter valid numbers in all fields.")
        except Exception as e:
            messagebox.showinfo("Error", str(e))

        return

    def select_source_files(self):

        self.clean_data()  # Clear any existing values in the entry fields

        if not self.validation_name():  # Validate first
            return  # Exit early if validation fails

        self.lora_name_version = self.lora_name_version  # Set LORA variable

        # Prompt the user to select an input directory
        dir_path = filedialog.askdirectory(title="Select input directory")

        if not dir_path:  # Handle case where the user cancels the directory selection
            print("No directory selected. Operation canceled.")
            return

        # Count the number of files (assuming every image has a corresponding pair, hence divided by 2)
        total_images: int =  int(FileUtils.count_files(dir_path) / 2)

        if total_images <= 0:  # If the folder is empty, exit early
            print("Empty folder")
            return

        # Update the UI with the selected source directory
        self.labelTitle.configure(text=f'Source: {os.path.basename(dir_path)}')

        # Insert the new values into the respective input fields
        self.source.insert(0, dir_path)
        self.total_files.insert(0, total_images)

        # Default values for epochs, batch size, and repetitions
        default_epochs = 1
        default_batch_size = 1
        default_repetitions = 20

        self.total_epochs.insert(0, default_epochs)
        self.total_batch.insert(0, default_batch_size)
        self.total_repeats.insert(0, default_repetitions)

        # Calculate the total training steps
        total_steps: int = int((
            total_images * default_epochs * default_repetitions) / default_batch_size)
        self.total_steps.insert(0, total_steps)
        
        return

    def validation_name(self):
        if (self.siderbar_loraValue.get() == ""):
            messagebox.showinfo("Warning", "No lora name")
            return False
        else:            
            new_name = self.siderbar_loraValue.get()
            self.lora_name_version = new_name + "_v" + self.lora_version

            return True

    def clean_data(self):
        self.source.delete(0, tkinter.END)
        self.total_files.delete(0, tkinter.END)
        self.total_epochs.delete(0, tkinter.END)
        self.total_batch.delete(0, tkinter.END)
        self.total_repeats.delete(0, tkinter.END)
        self.total_steps.delete(0, tkinter.END)
        self.labelTitle.configure(text=f'Lora Helper :')
        return

    def finish_button_event(self):
        messagebox.showinfo("Complete", "Done")

    def create_training_structures(self):
        lora_structure = Lora(self.path, self.lora_name, self.lora_name_version, self.lora_version, self.source.get(),
                                   self.total_repeats.get(), self.total_files.get(), self.total_epochs.get(), self.total_batch.get(), self.total_steps.get())
        lora_utils = LoraUtils(lora_structure)
        lora_utils.create_lora_structure()
        self.finish_button_event()