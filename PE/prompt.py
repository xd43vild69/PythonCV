class Prompt:
    positive = ""
    negative = ""
    sampler = ""
    CFG = ""
    seed = ""
    size = ""
    modelHash = ""
    model = ""
    vaeHash = ""
    vae = ""
    clipSkip = ""
    aDetailer = ""
    aDetailerConfidence = ""
    FaceRestoration = ""
    block = ""
    currentState = "Positive"

    def nextStatus(self, status):

        match status:
            case str(x) if "Negative" in x:
                self.currentState = "Negative"
            case str(x) if "Sampler" in x:
                self.currentState = "Sampler"  
            case str(x) if "CFG" in x:
                self.currentState = "CFG"  
            case str(x) if "Seed" in x:
                self.currentState = "Seed"      
            case str(x) if "Size" in x:
                self.currentState = "Size"         
            case str(x) if "Model hash" in x:
                self.currentState = "Model hash"
            case str(x) if "Model" in x:
                self.currentState = "Model"         
            case str(x) if "VAE hash" in x:
                self.currentState = "VAE hash"         
            case str(x) if "VAE" in x:
                self.currentState = "VAE"                              
            case str(x) if "Clip skip" in x:
                self.currentState = "Clip skip"
            case str(x) if "ADetailer" in x:
                self.currentState = "ADetailer"                       
            case str(x) if "ADetailer confidence" in x:
                self.currentState = "ADetailer confidence"
            case str(x) if "Face restoration" in x:
                self.currentState = "Face restoration"
            case _:
                self.currentState = self.currentState


    def addValue(self, value):
        match self.currentState:
            case "Positive":
                self.positive = self.positive + value + ","
            case "Negative":
                self.negative = self.negative + value
            case "Sampler":
                self.sampler = self.sampler + value
            case "CFG":
                self.CFG = self.CFG + value
            case "Seed":
                self.seed = self.seed + value
            case "Size":
                self.size = self.size + value
            case "Model hash":
                self.modelHash = self.modelHash + value
            case "Model":
                self.model = self.model + value
            case "VAE hash":
                self.vaeHash = self.vaeHash + value
            case "VAE":
                self.vae = self.vae + value
            case "Clip skip":
                self.clipSkip = self.clipSkip + value
            case "ADetailer":
                self.aDetailer = self.aDetailer + value
            case "Face restoration":
                self.FaceRestoration = self.FaceRestoration + value
            case "ADetailer confidence":
                self.aDetailerConfidence = self.aDetailerConfidence + value
        return