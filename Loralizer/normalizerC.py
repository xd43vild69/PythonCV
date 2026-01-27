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

class NormalizerC:
    def __init__(self, input_dir, destination_dir, trigger_word, target_size=1024):
        self.output_dir = destination_dir
        self.__attr = input_dir
        self.trigger_word = trigger_word
        self.target_size = target_size
        # Crear directorio de salida si no existe
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.process(input_dir)

    output_dir = ""

    trigger_word = ""
    # Template mejorado para Ollama
    ollama_model = "llava"
    ollama_prompt = """You are generating captions for training a Character LoRA. 
Analyze the image and describe ONLY elements that should NOT be learned as part of the character identity. 
Describe clothing, accessories, background, environment, and any objects present. 
Do NOT describe facial features, skin tone, body characteristics, hairstyle, hair color, or any physical traits of the character. 
Do NOT describe image style, lighting, camera, or composition. 
Do NOT add explanations or commentary. 
Write a concise natural language caption suitable for dataset training. 
Return ONLY the caption."""

    @property
    def attr(self):  
        return self.__attr

    def process(self, input_dir):
        """Procesa todas las imágenes en el directorio de entrada"""
        image_formats = ('*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.tiff')
        image_paths = []
        
        # Recolectar todas las rutas de imágenes
        for format in image_formats:
            image_paths.extend(glob(os.path.join(input_dir, format)))
        
        print(f"Found {len(image_paths)} images. Processing images...")   
        
        try:
            counter = 1
            # Procesar cada imagen
            for image_path in image_paths:
                try:
                    print(f"Processing image {counter}/{len(image_paths)}: {os.path.basename(image_path)}")
                    image = cv2.imread(image_path)

                    if image is None:
                        print(f"Failed to read image: {image_path}")
                        continue

                    # Normalizar la imagen
                    self.square_image(image, image_path, counter, size=(self.target_size, self.target_size))
                    counter += 1

                except cv2.error as e:
                    print(f"OpenCV error while processing {image_path}: {e}")
                except Exception as e:
                    print(f"An error occurred with image {image_path}: {e}")

            print(f"\nData normalization completed. Processed {counter-1} images.")

        except KeyboardInterrupt:
            print("\nData normalization interrupted by the user.")
            sys.exit(0)

    def square_image(self, img, image_path, counter, size=(1024, 1024)):
        """Convierte la imagen a cuadrada de size x size y genera caption"""
        # Definir ruta de salida
        output_image_path = os.path.join(self.output_dir, f"n_{counter}.png")
        
        # Obtener dimensiones originales
        h, w = img.shape[:2]
        c = img.shape[2] if len(img.shape) > 2 else 1

        # Si la imagen ya es cuadrada, solo redimensionar
        if h == w:
            resized = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
            cv2.imwrite(output_image_path, resized)
            print(f"  → Saved: {os.path.basename(output_image_path)}")
            self.generate_caption(output_image_path)
            return

        # Crear imagen cuadrada centrada
        larger_dim = max(h, w)
        interpolation = cv2.INTER_AREA if larger_dim > sum(size) // 2 else cv2.INTER_CUBIC

        # Crear máscara negra
        if c == 1:
            mask = np.zeros((larger_dim, larger_dim), dtype=img.dtype)
        else:
            mask = np.zeros((larger_dim, larger_dim, c), dtype=img.dtype)

        # Centrar imagen original
        x_offset = (larger_dim - w) // 2
        y_offset = (larger_dim - h) // 2
        mask[y_offset:y_offset + h, x_offset:x_offset + w] = img

        # Redimensionar a tamaño final
        resized = cv2.resize(mask, size, interpolation=interpolation)

        # Guardar imagen procesada
        cv2.imwrite(output_image_path, resized)
        print(f"  → Saved: {os.path.basename(output_image_path)}")
        
        # Generar caption
        self.generate_caption(output_image_path)

    def generate_caption(self, image_path):
        """Genera un caption para la imagen usando Ollama/LLaVA"""
        txt_path = os.path.splitext(image_path)[0] + ".txt"
        
        try:
            print(f"  → Generating caption...")
            caption = self.caption_with_ollama(image_path)
            caption = caption + ", " + self.trigger_word
            # Guardar caption en archivo .txt
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(caption)
            
            print(f"  → Caption saved: {os.path.basename(txt_path)}")
            print(f"  → Caption preview: {caption[:100]}{'...' if len(caption) > 100 else ''}")
            
        except Exception as e:
            print(f"  → Error generating caption: {e}")
            # Guardar un caption vacío o de fallback
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write("Error generating caption")

    def caption_with_ollama(self, image_path, timeout=60):
        """Genera caption usando Ollama con modelo LLaVA"""
        try:
            # Comando para Ollama con imagen
            cmd = [
                "ollama", "run", self.ollama_model,
                self.ollama_prompt
            ]
            
            # Ejecutar Ollama y pasar la imagen
            result = subprocess.run(
                cmd,
                input=f"Analyze this image: {image_path}",
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if result.returncode != 0:
                raise RuntimeError(f"Ollama failed: {result.stderr}")
            
            caption = result.stdout.strip()
            
            # Limpiar el caption
            caption = caption.replace('\n', ' ').strip()
            
            return caption if caption else "No caption generated"
            
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"Ollama timed out after {timeout} seconds")
        except FileNotFoundError:
            raise RuntimeError("Ollama not found. Make sure it's installed and in PATH")

# -----------------------
# Helper captioner utils
# -----------------------

def caption_with_command(cmd_template, image_path, timeout=30):
    """
    Ejecuta un comando shell para producir un caption.
    cmd_template: string con formato donde '{image_path}' será reemplazado.
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
    Envía imagen (base64) + prompt a un endpoint HTTP y retorna el caption.
    """
    if requests is None:
        raise RuntimeError("requests library required (pip install requests)")
    
    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    
    payload = {
        "model": model,
        "prompt": prompt_template.format(path=image_path),
        "image_b64": b64
    }
    
    headers = {"Content-Type": "application/json"}
    resp = requests.post(endpoint, data=json.dumps(payload), headers=headers, timeout=timeout)
    resp.raise_for_status()
    
    try:
        j = resp.json()
        return j.get("caption") or j.get("text") or json.dumps(j, ensure_ascii=False)
    except Exception:
        return resp.text


# -----------------------
# Ejemplo de uso
# -----------------------
if __name__ == "__main__":
    # Opción 1: Usar diálogos de selección de carpetas
    print("Select INPUT folder with images...")
    input_folder = filedialog.askdirectory(title="Select INPUT folder")
    
    if not input_folder:
        print("No input folder selected. Exiting.")
        sys.exit(1)
    
    print("Select OUTPUT folder for normalized images...")
    output_folder = filedialog.askdirectory(title="Select OUTPUT folder")
    
    if not output_folder:
        print("No output folder selected. Exiting.")
        sys.exit(1)
    
    # Crear instancia y procesar
    normalizer = Normalizer(input_folder, output_folder)
    
    # Opción 2: Usar rutas hardcoded (comentar/descomentar según necesites)
    # normalizer = Normalizer("./input_images", "./output_normalized")