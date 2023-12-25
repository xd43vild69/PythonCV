import os
import sys
import random
import cv2
import numpy as np
import tkinter as tk
from glob import glob
from tkinter import filedialog

def flip_image(image):
    result = cv2.flip(image, 1)
    return result

# Hide the main tkinter window
root = tk.Tk()
root.withdraw()

# Ask user to select input directory
print("Please select the input directory...")
input_dir = filedialog.askdirectory(title="Select input directory")

# Ask user to select output directory
print("Please select the output directory...")
output_dir = filedialog.askdirectory(title="Select output directory")

# If output directory does not exist, create it
if not os.path.exists(output_dir):
	os.makedirs(output_dir)

# Process images in input directory
image_formats = ('*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.tiff')
image_paths = []
for format in image_formats:
	image_paths.extend(glob(os.path.join(input_dir, format)))

# Get user input for data augmentation parameters
num_rotations = 2 #int(input("Enter the number of rotations for each image: "))
num_crops = 4 #int(input("Enter the number of random crops for each image: "))
num_contrasts = 0 #int(input("Enter the number of contrast adjustments for each image: "))
num_brightnesses = 2 #int(input("Enter the number of brightness adjustments for each image: "))

print("Processing images...")

try:
	# Loop through all image files in the input directory
	for image_path in image_paths:
		print(f"Processing image: {image_path}")

		# Read the image
		image = cv2.imread(image_path)

		# Save a copy of the original image
		original_image_path = os.path.join(output_dir, f"orig_{os.path.splitext(os.path.basename(image_path))[0]}.png")
		cv2.imwrite(original_image_path, image)

		# Perform specified flip
		flipped_image = flip_image(image)
		flippped_image_path = os.path.join(output_dir, f"flip_{os.path.splitext(os.path.basename(image_path))[0]}.png")
		cv2.imwrite(flippped_image_path, flipped_image)
		print(f"Saved flip image: {flippped_image_path}")

	print("Data augmentation completed.")

except KeyboardInterrupt:
	print("Data augmentation interrupted by the user.")
	sys.exit(0)