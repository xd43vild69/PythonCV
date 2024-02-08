class Prompt:

    positive = ""
    negative = ""
    sampler = ""
    CFG = ""
    seed = ""
    steps = ""
    size = ""
    modelHash = ""
    model = ""
    vaeHash = ""
    vae = ""
    clipSkip = ""
    aDetailer = ""
    aDetailerConfidence = ""
    aDetailerPrompt = ""
    faceRestoration = ""
    block = ""
    currentState = "Positive:"

    def nextStatus(self, status):
        # if there is a crlf \n we need to handle it
        match status:
            case str(x) if "Negative prompt:" in x:
                self.currentState = "Negative prompt:"
            case str(x) if "Steps:" in x:
                self.currentState = "Steps:"                  
            case str(x) if "Sampler:" in x:
                self.currentState = "Sampler:"  
            case str(x) if "CFG scale:" in x:
                self.currentState = "CFG scale:"  
            case str(x) if "Seed:" in x:
                self.currentState = "Seed:"      
            case str(x) if "Size:" in x:
                self.currentState = "Size:"         
            case str(x) if "Model hash:" in x:
                self.currentState = "Model hash:"
            case str(x) if "Model:" in x:
                self.currentState = "Model:"         
            case str(x) if "VAE hash:" in x:
                self.currentState = "VAE hash:"         
            case str(x) if "VAE:" in x:
                self.currentState = "VAE:" 
            case str(x) if "Clip skip:" in x:
                self.currentState = "Clip skip:"
            case str(x) if "ADetailer model:" in x:
                self.currentState = "ADetailer model:"                       
            case str(x) if "ADetailer prompt:" in x:
                self.currentState = "ADetailer prompt:"
            case str(x) if "Face restoration:" in x:
                self.currentState = "Face restoration:"
            case _:
                self.currentState = self.currentState


    def addValue(self, value):
        match self.currentState:
            case "Positive:":
                self.positive = self.positive + value + ","
            case "Negative prompt:":
                self.negative = self.negative + value.replace("Negative prompt:", "") + ","
            case "Steps:":
                self.steps = self.steps + value.replace("Steps:", "")
            case "Sampler:":
                self.sampler = self.sampler + value.replace("Sampler:", "")
            case "CFG scale:":
                self.CFG = self.CFG + value.replace("CFG scale:", "")
            case "Seed:":
                self.seed = self.seed + value.replace("Seed:", "")
            case "Size:":
                self.size = self.size + value.replace("Size:", "")
            case "Model hash:":
                self.modelHash = self.modelHash + value.replace("Model hash:", "")
            case "Model:":
                self.model = self.model + value.replace("Model:", "")
            case "VAE hash:":
                self.vaeHash = self.vaeHash + value.replace("VAE hash:", "")
            case "VAE:":
                self.vae = self.vae + value.replace("VAE:", "")
            case "Clip skip:":
                self.clipSkip = self.clipSkip + value.replace("Clip skip:", "")
            case "ADetailer model:":
                self.aDetailer = self.aDetailer + value + ","
            case "ADetailer prompt:":
                self.aDetailer = self.aDetailerPrompt + value + ","
            case "Face restoration:":
                self.faceRestoration = self.faceRestoration + value
            case "ADetailer confidence":
                self.aDetailerConfidence = self.aDetailerConfidence + value
        return