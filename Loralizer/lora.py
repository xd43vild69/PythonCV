class Lora:
     
    def __init__(self):
        super().__init__()
        self.pathx = ""

    def update_base(self, path, name, lora, version, source, total_repetitions, total_files, total_epochs, total_batch, total_steps):    
        self.path = path # absolute_path
        self.lora_name = name # f'{lora_version}_lora_{LORA}'
        self.LORA = lora
        self.lora_version = version
        self.source = source #sourceEntry.get()
        self.total_repeats = total_repetitions #quantityRepeatition.get()        
        self.total_files = total_files # self.quantityFiles.get()
        self.total_epochs = total_epochs # self.quantityEpochs.get()
        self.total_batch = total_batch # self.quantityBatchSize.get()
        self.total_steps = total_steps # self.quantityTotalTrain.get()

    def u(self):
        s = ""

    def update_caculation(self, total_files, total_epochs, total_batch, total_steps):
        self.total_files =total_files
        self.total_epochs =total_epochs
        self.total_batch =total_batch
        self.total_steps = total_steps

        