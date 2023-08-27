import os

class LoraCalculations:
    def __init__(self):
        return

    def Calculation(self):
        return "c"
    
    def countFolderFiles(dir_path):
        count = 0
        for path in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, path)):
                count += 1
        return count