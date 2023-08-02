import os
import sys
import random
import cv2
import numpy as np
import tkinter as tk
from glob import glob
from tkinter import filedialog
import uuid

def flip_image(image):
    result = cv2.flip(image, 1)
    return result

def rotate_image(image, angle):
    center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
    return result

def random_crop(image, min_crop_size):
    height, width = image.shape[:2]
    if height < min_crop_size or width < min_crop_size:
        return image
    crop_size = random.randint(min_crop_size, min(height, width))
    x = random.randint(0, width - crop_size)
    y = random.randint(0, height - crop_size)
    return image[y:y+crop_size, x:x+crop_size]

def adjust_brightness_contrast(image, brightness=0, contrast=0):
    return cv2.addWeighted(image, 1 + float(contrast) / 100.0, image, 0, float(brightness))

def loop_rotate(image, num_rotations):
    for j in range(num_rotations):
        angle = random.uniform(-10, 10)
        rotated_image = rotate_image(image, angle)
        rotated_image_path = os.path.join(output_dir, f"rot{j+1}_{os.path.splitext(os.path.basename(image_path))[0]}.png")
        cv2.imwrite(rotated_image_path, rotated_image)
        print(f"Saved rotated image: {rotated_image_path}")

def loop_crop(image, num_crops):
    for j in range(num_crops):
        cropped_image = random_crop(image, 512)
        cropped_image_path = os.path.join(output_dir, f"cro{j+1}_{os.path.splitext(os.path.basename(image_path))[0]}.png")
        cv2.imwrite(cropped_image_path, cropped_image)
        print(f"Saved cropped image: {cropped_image_path}")

def loop_contrast_2(image):
    contrast = 14
    for j in range(2):            
        contrasted_image = adjust_brightness_contrast(image, contrast=contrast)
        contrasted_image_path = os.path.join(output_dir, f"contrast_{j+1}_{os.path.splitext(os.path.basename(image_path))[0]}.png")
        cv2.imwrite(contrasted_image_path, contrasted_image)
        print(f"Saved contrast-adjusted image: {contrasted_image_path}")
        contrast = contrast * -1

def loop_contrast(image, num_contrasts):
    for j in range(num_contrasts):
        contrast = 14 #, random.uniform(0.2, 2.0)
        contrasted_image = adjust_brightness_contrast(image, contrast=contrast)
        contrasted_image_path = os.path.join(output_dir, f"contrast_{j+1}_{os.path.splitext(os.path.basename(image_path))[0]}.png")
        cv2.imwrite(contrasted_image_path, contrasted_image)
        print(f"Saved contrast-adjusted image: {contrasted_image_path}")

def loop_brightness(image, num_brightnesses):
    for j in range(num_brightnesses):
        brightness = random.uniform(-100, 100)
        brightened_image = adjust_brightness_contrast(image, brightness=brightness)
        brightened_image_path = os.path.join(output_dir, f"brightness_{j+1}_{os.path.splitext(os.path.basename(image_path))[0]}.png")
        cv2.imwrite(brightened_image_path, brightened_image)
        print(f"Saved brightness-adjusted image: {brightened_image_path}")

def loop_flip(image):
    flipped_image = flip_image(image)
    flippped_image_path = os.path.join(output_dir, f"flip_{os.path.splitext(os.path.basename(image_path))[0]}_{uuid.uuid4()}.png")
    cv2.imwrite(flippped_image_path, flipped_image)
    print(f"Saved flip image: {flippped_image_path}")

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
num_crops = 6 #int(input("Enter the number of random crops for each image: "))
num_contrasts = 1 #int(input("Enter the number of contrast adjustments for each image: "))
num_brightnesses = 0 #int(input("Enter the number of brightness adjustments for each image: "))

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

        # Perform specified number of rotations and save copies
        loop_rotate(image, num_rotations)
    
        # Randomly crop the image with a minimum size of 512x512 and save copies
        loop_crop(image, num_crops)

        # Perform specified number of contrast adjustments and save copies
        loop_contrast_2(image)

        # Perform specified number of brightness adjustments and save copies
        loop_brightness(image, num_brightnesses)

        # Perform specified flip
        

    print("Data augmentation completed.")

except KeyboardInterrupt:
    print("Data augmentation interrupted by the user.")
    sys.exit(0)