from pathlib import Path
from distutils.dir_util import copy_tree
import datetime
import uuid
import os
from pathlib import Path
import pathlib
from file_utils import FileUtils
from lora import Lora
import glob


class LoraUtils:

    def __init__(self, lora: Lora):
        super().__init__()
        self.lora = lora
        self.logging_dir = ""
        self.output_dir_15 = ""
        self.output_dir_xl = ""
        self.output_dir_flux = ""
        self.train_data_dir = ""
        self.output_lora = ""
        self.sample_prompts = ""

    def get_last_lora_version(self):
        try:
            with open("LoraCounter.txt", "r") as file:
                lora_version = int(file.read()) + 1
        except (FileNotFoundError, ValueError):
            lora_version = 1

        with open("LoraCounter.txt", "w") as file:
            file.write(str(lora_version))

        return lora_version

    def get_lora_training_folder(self):
        try:
            with open("LoraCTrainingFolder.txt", "r") as file:
                lora_training_folder = file.read().strip()
        except FileNotFoundError:
            lora_training_folder = ""
        except Exception as e:
            lora_training_folder = ""
        return lora_training_folder

    def create_lora_structure(self):
        try:
            path_dir = Path(self.lora.source)
            # Base directory for the Lora model
            lora_base_path = Path(self.lora.path) / self.lora.lora_name

            # List of subdirectories to create
            subdirs = [
                'image',
                'log',
                'model_15',
                'model_xl',
                'model_flux',
                f'image/{self.lora.total_repeats}_{self.lora.LORA}'
            ]

            # Create base directory if it doesn't exist
            if not lora_base_path.exists():
                lora_base_path.mkdir(parents=True)

                # Create subdirectories
                for subdir in subdirs:
                    (lora_base_path / subdir).mkdir(parents=True)

                # Copy source files to the new image directory
                copy_tree(str(path_dir), str(lora_base_path /
                          f'image/{self.lora.total_repeats}_{self.lora.LORA}'))

                # Create log and configuration files
                self.createLog(str(lora_base_path))
                self.createConfigJson_15()
                self.createConfigJsonXL()
                self.createConfigJsonFlux()
                self.set_lora_keyword()
            else:
                print("Folder already exists")
        except Exception as e:
            print("Folder already exists", str(e))

        return

    def createLog(self, path):
        # Generate a unique filename for the log
        file_name = os.path.join(
            path, f'log-{datetime.date.today()}_{uuid.uuid4()}.txt')

        # Create a log message with configuration details
        log_message = (
            f'Quantity files: {self.lora.total_files}, '
            f'Quantity epochs: {self.lora.total_epochs}, '
            f'Quantity batch size: {self.lora.total_batch}, '
            f'Quantity repeats: {self.lora.total_repeats}, '
            f'Total steps: {self.lora.total_steps}'
        )

        try:
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(log_message)
        except Exception as e:
            print(f"Error creating log file: {e}")

        return

    def createConfigJson_15(self):
        with open('LoraD13.json', 'r') as file:
            data = file.readlines()

        data[59] = r"" + self.output_dir_15.replace("\\", "\/") + "\n"
        data[60] = r"" + self.output_lora.replace("\\", "\/") + "\n"
        data[70] = r"" + self.train_data_dir.replace("\\", "\/") + "\n"
        data[86] = self.sample_prompts + "\n"

        self.set_to_disk(data, "15")
        return

    def createConfigJsonXL(self):
        with open('LoraD13_XL.json', 'r') as file:
            data = file.readlines()

        data[61] = r"" + self.logging_dir.replace("\\", "\/") + "\n"
        data[104] = r"" + self.output_dir_xl.replace("\\", "\/") + "\n"
        data[105] = r"" + self.output_lora.replace("\\", "\/") + "\n"
        data[140] = r"" + self.train_data_dir.replace("\\", "\/") + "\n"
        data[118] = self.sample_prompts + "\n"

        self.set_to_disk(data, "xl")
        return

    def createConfigJsonFlux(self):
        with open('LoraD13_Flux.json', 'r') as file:
            data = file.readlines()

        data[122] = r"" + self.output_dir_flux.replace("\\", "\/") + "\n"
        data[123] = r"" + self.output_lora.replace("\\", "\/") + "\n"
        data[165] = r"" + self.train_data_dir.replace("\\", "\/") + "\n"
        data[136] = self.sample_prompts + "\n"

        self.set_to_disk(data, "flux")
        return

    def get_initial_config(self):
        self.logging_dir = f'  \"logging_dir\":\"{self.lora.path}\\{self.lora.lora_version}_lora_{self.lora.LORA}\\log", '
        self.output_dir_15 = f'  \"output_dir\":\"{pathlib.PureWindowsPath(self.lora.path)}\\{self.lora.lora_version}_lora_{self.lora.LORA}\\model_15", '
        self.output_dir_xl = f'  \"output_dir\":\"{pathlib.PureWindowsPath(self.lora.path)}\\{self.lora.lora_version}_lora_{self.lora.LORA}\\model_xl", '
        self.output_dir_flux = f'  \"output_dir\":\"{pathlib.PureWindowsPath(self.lora.path)}\\{self.lora.lora_version}_lora_{self.lora.LORA}\\model_flux", '
        self.train_data_dir = f'  \"train_data_dir\":\"{pathlib.PurePath(self.lora.path)}\\{self.lora.lora_version}_lora_{self.lora.LORA}\\image", '
        self.output_lora = f'  \"output_name\":\"{self.lora.LORA}", '
        self.sample_prompts = f'  \"sample_prompts\":\"{FileUtils.getInitialPrompt("")}", '

    def set_to_disk(self, data, version):
        config_file = Path(self.lora.path) / self.lora.lora_name / \
            f'lora_config_{self.lora.LORA}_{version}.json'
        if not os.path.exists(config_file):
            with open(config_file, 'w') as file:
                file.writelines(data)

    def set_lora_keyword(self):

        path_init = str(Path(self.lora.path) / self.lora.lora_name /
                        "image" / f'{self.lora.total_repeats}_{self.lora.LORA}')

        files = glob.glob(path_init + "\\*.txt")
        data = ""
        for file in files:
            try:
                with open(file, 'r') as f:
                    data = f.readlines()
                dataAlteration = self.lora.LORA + ", " + data[0]
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(dataAlteration)
            except:
                print("Keyword exception on file")

        return
