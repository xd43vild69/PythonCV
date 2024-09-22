import pathlib
import os

class ConfigManager:
    
    def create_config_json(self, absolute_path, lora_version, lora_name, template_path, model_type="15"):
        with open(template_path, 'r') as file:
            data = file.readlines()

        output_dir = f'  \"output_dir\":\"{pathlib.PureWindowsPath(absolute_path)}\\{lora_version}_lora_{lora_name}\\model_{model_type}\", '
        train_data_dir = f'  \"train_data_dir\":\"{absolute_path}\\{lora_version}_lora_{lora_name}\\image\", '
        output_lora = f'  \"output_name\":\"{lora_name}\", '

        # Edit config lines
        data[59] = output_dir.replace("\\", "\/") + "\n"
        data[60] = output_lora.replace("\\", "\/") + "\n"
        data[70] = train_data_dir.replace("\\", "\/") + "\n"
        
        config_file = f'{absolute_path}\\{lora_version}_lora_{lora_name}\\lora_config_{lora_name}_{model_type}.json'
        if not os.path.exists(config_file):
            with open(config_file, 'w') as file:
                file.writelines(data)