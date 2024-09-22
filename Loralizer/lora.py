class Lora:
     
    def __init__(self):
        super().__init__()
        self.pathx = ""

    def update_base(self, path, name, lora, version, source, total_repetitions, total_files, total_epochs, total_batch, total_steps):    
        self.path = path 
        self.lora_name = name
        self.LORA = lora
        self.lora_version = version
        self.source = source 
        self.total_repeats = total_repetitions 
        self.total_files = total_files 
        self.total_epochs = total_epochs
        self.total_batch = total_batch 
        self.total_steps = total_steps 

    def update_caculation(self, total_files, total_epochs, total_batch, total_steps):
        self.total_files =total_files
        self.total_epochs =total_epochs
        self.total_batch =total_batch
        self.total_steps = total_steps

        