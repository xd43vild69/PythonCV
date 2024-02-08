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
    denoiseStrength = ""
    clipSkip = ""
    aDetailerModel = ""
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
            case str(x) if "Denoising strength:" in x:
                self.currentState = "Denoising strength:"
            case str(x) if "Clip skip:" in x:
                self.currentState = "Clip skip:"
            case str(x) if "ADetailer model:" in x:
                self.currentState = "ADetailer model:"                       
            case str(x) if "ADetailer prompt:" in x:
                self.currentState = "ADetailer prompt:"
            case str(x) if "Face restoration:" in x:
                self.currentState = "Face restoration:"
            case str(x) if "ADetailer confidence:" in x:
                self.currentState = "x.13"
            case str(x) if "x.13" in x:
                self.currentState = "x.13"
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
            case "Denoising strength:":
                self.denoiseStrength = self.denoiseStrength + value.replace("Denoising strength:", "")
            case "Clip skip:":
                self.clipSkip = self.clipSkip + value.replace("Clip skip:", "")
            case "ADetailer model:":
                self.aDetailerModel = self.aDetailerModel + value.replace("ADetailer model:", "")
            case "ADetailer prompt:":
                self.aDetailerPrompt = self.aDetailerPrompt + value.replace("ADetailer prompt:", "") + ","
            case "Face restoration:":
                self.faceRestoration = self.faceRestoration + value
            case "ADetailer confidence":
                self.aDetailerConfidence = self.aDetailerConfidence + value
        return