import os
from tkinter import filedialog
import glob

class FileUtils:

    @staticmethod
    def count_files(dir_path):
        count = 0
        for path in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, path)):
                count += 1
        return count

    @staticmethod
    def create_log(path, log_message):
        file_name = os.path.join(path, f'log.txt')
        try:
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(log_message)
        except Exception as e:
            print(f"Error creating log file: {e}")

    @staticmethod
    def get_last_lora_version():
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

    @staticmethod
    def get_lora_training_folder():
        try:
            with open("LoraCTrainingFolder.txt", "r") as file:
                # Use strip() to remove any extra whitespace or newlines
                lora_training_folder = file.read().strip()
        except FileNotFoundError:
            print("LoraCTrainingFolder.txt not found.")
            lora_training_folder = ""
        except Exception as e:
            print(f"An error occurred: {e}")
            lora_training_folder = ""

        return lora_training_folder

    @staticmethod
    def getInitialPrompt(path_init):
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
