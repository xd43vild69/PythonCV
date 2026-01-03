import cv2
import numpy as np
import os
import sys
from glob import glob
from tkinter import filedialog
import subprocess
import base64
import json

try:
    import requests
except Exception:
    requests = None

class Normalizer:
    def __init__(self, input_dir, destination_dir):
        self.output_dir = destination_dir     
        self.process(input_dir)
        self.__attr = input_dir    
        pass

    # Additional normalization methods

    output_dir = ""
    #ollama_template = "ollama run llava You are an expert at training LoRA and preparing a dataset for Character LoRA. First describe this picture in natural language. Then, Prepare the caption for this image, assuming we are training a Character LoRA for the main subject in this image on z image turbo using natural language, using each and every one of these captioning categories"
    # ollama_template = "ollama run redule26/huihui_ai_qwen2.5-vl-7b-abliterated You are preparing captions for training a Character LoRA. Analyze the image and return ONLY a concise natural language description of the main character. Return ONLY the character description"
    #ollama_template = "ollama run redule26/huihui_ai_qwen2.5-vl-7b-abliterated You are generating captions for training a Character LoRA. Analyze the image and return ONLY a concise natural language description of the main character’s identity. Return ONLY the character identity description."
    
    # Descriptive version for not losing important details
    #ollama_template = "ollama run redule26/huihui_ai_qwen2.5-vl-7b-abliterated You are generating captions for training a Character LoRA. Assume an image is already provided. Analyze the image and return ONLY a concise natural language description of the main character’s identity. Focus exclusively on persistent character traits: facial features, body structure, skin tone, hairstyle and hair color, distinctive marks, recurring clothing style, overall aesthetic identity. Rules: Do NOT describe background, environment, pose, or action. Do NOT mention lighting, camera, composition, or image quality. Do NOT describe temporary emotions or expressions. Do NOT ask for the image. Do NOT add explanations or commentary. Write a single neutral paragraph suitable for dataset training. Return ONLY the character identity description."
    
    # Descriptive version for better results
    ollama_template = "ollama run redule26/huihui_ai_qwen2.5-vl-7b-abliterated You are generating captions for training a Character LoRA. Assume an image is already provided. Analyze the image and describe ONLY elements that should NOT be learned as part of the character identity. Describe clothing, accessories, background, environment, and any objects present. Do NOT describe facial features, skin tone, body characteristics, hairstyle, hair color, or any physical traits of the character. Do NOT describe image style, lighting, camera, or composition. Do NOT add explanations or commentary. Write a concise natural language caption suitable for dataset training. Return ONLY the caption."



    @property
    def attr(self):  
        return self.__attr

    def process(self, input_dir):
        # Process images in input directory
        image_formats = ('*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.tiff')
        image_paths = []
        
        for format in image_formats:
            image_paths.extend(glob(os.path.join(input_dir, format)))
        
        print(f"Found {len(image_paths)} images. Processing images...")   
        try:
            counter = 1
            # Loop through all image files in the input directory
            for image_path in image_paths:
                try:
                    print(f"Processing image: {image_path}")
                    image = cv2.imread(image_path)

                    if image is None:
                        print(f"Failed to read image: {image_path}")
                        continue

                    # Normalize the image by resizing or processing
                    self.square_image_1024(image, image_path, counter)
                    counter += 1

                except cv2.error as e:
                    print(f"OpenCV error while processing {image_path}: {e}")
                except Exception as e:
                    print(f"An error occurred with image {image_path}: {e}")

            print("Data normalization completed.")

        except KeyboardInterrupt:
            print("Data normalization interrupted by the user.")
            sys.exit(0)

    def square_image_1024(self, img, image_path, counter, size=(1024, 1024)):
        # Define the output file path
        output_image_path = os.path.join(self.output_dir, f"n_{counter}.png")
        
        # Get the original image dimensions
        h, w = img.shape[:2]
        c = img.shape[2] if len(img.shape) > 2 else 1  # Number of color channels (c)

        # If the image is already square, just resize it directly
        if h == w:
            resized = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
            cv2.imwrite(output_image_path, resized)
            return

        # Determine the new square dimension (whichever is larger between height and width)
        larger_dim = max(h, w)

        # Choose the interpolation method based on the size of the image
        interpolation = cv2.INTER_AREA if larger_dim > sum(size) // 2 else cv2.INTER_CUBIC

        # Create a square mask with black background
        if c == 1:
            mask = np.zeros((larger_dim, larger_dim), dtype=img.dtype)
        else:
            mask = np.zeros((larger_dim, larger_dim, c), dtype=img.dtype)

        # Center the original image on the mask
        x_offset = (larger_dim - w) // 2
        y_offset = (larger_dim - h) // 2
        mask[y_offset:y_offset + h, x_offset:x_offset + w] = img

        # Resize the centered image to the desired output size
        resized = cv2.resize(mask, size, interpolation=interpolation)

        # Save the resulting image to the output path
        cv2.imwrite(output_image_path, resized)

        cmd = self.ollama_template + ": {image_path}'"
        self.generate_caption(output_image_path, cmd)


    def generate_caption(self, image_path, cmd_template):
        """
        Genera un caption para la imagen dada y lo guarda en un archivo .txt.
        """
        try:
            caption = caption_with_command(cmd_template, image_path)
            txt_path = os.path.splitext(image_path)[0] + ".txt"
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(caption)
        except Exception as e:
            
            txt_path = os.path.splitext(e.__annotations__)[0] + ".txt"
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(caption)            
            print(f"Error generating caption for {image_path}: {e}")

# -----------------------
# Helper captioner utils
# -----------------------

def caption_with_command(cmd_template, image_path, timeout=30):
    """
    Run a shell command to produce a caption.
    cmd_template: a format string where '{image_path}' will be replaced.
    Example: "ollama run mymodel --prompt 'Caption the image {image_path}'"
    Returns command stdout decoded as UTF-8.
    """
    cmd = cmd_template.format(image_path=image_path)
    result = subprocess.run(cmd, shell=True, capture_output=True, timeout=timeout)
    out = result.stdout.decode("utf-8", errors="replace").strip()
    if result.returncode != 0:
        err = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"Command failed (rc={result.returncode}): {err}")
    return out

def caption_via_http(endpoint, model, prompt_template, image_path, timeout=30):
    """
    POST image (base64) + prompt to an HTTP endpoint and return the response text.
    Assumes the endpoint accepts JSON: { "model": ..., "prompt": ..., "image_b64": "..." }.
    The response can be plain text or JSON; this function returns JSON['caption'] if present,
    otherwise response.text.
    """
    if requests is None:
        raise RuntimeError("requests library is required for HTTP captioner (pip install requests)")
    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    payload = {"model": model, "prompt": prompt_template.format(path=image_path), "image_b64": b64}
    headers = {"Content-Type": "application/json"}
    resp = requests.post(endpoint, data=json.dumps(payload), headers=headers, timeout=timeout)
    resp.raise_for_status()
    try:
        j = resp.json()
        return j.get("caption") or j.get("text") or json.dumps(j, ensure_ascii=False)
    except Exception:
        return resp.text