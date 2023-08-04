import os
import sys
import tkinter as tk
from glob import glob
import cv2
from tkinter import filedialog

# Hide the main tkinter window
root = tk.Tk()
root.withdraw()

# Ask user to select input directory
print("Please select the input directory...")
input_dir = filedialog.askdirectory(title="Select input directory")

# Process images in input directory
image_formats = ('*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.tiff')
image_paths = []
for format in image_formats:
    image_paths.extend(glob(os.path.join(input_dir, format)))

print("Processing images...")

try:
    folder_counter = 0
    image_counter = 0
    image_top = 3
    output_dir = input_dir + "_split"
    
    
    for image_path in image_paths:
        
        image = cv2.imread(image_path)

        if not os.path.exists(output_dir + "/" + str(folder_counter)):
            os.makedirs(output_dir + "/" + str(folder_counter))

        original_image_path = os.path.join(output_dir + "/" + str(folder_counter), f"source_{os.path.splitext(os.path.basename(image_path))[0]}.png")
        cv2.imwrite(original_image_path, image)

        image_counter += 1

        if image_counter >= image_top:
            folder_counter += 1
            image_top += 3


    print("finished...")
except KeyboardInterrupt:
    print("Data splitted interrupted by the user.")
    sys.exit(0)