import cv2
import numpy as np
import os
import sys
from glob import glob
from tkinter import filedialog

class Normalizer:

    output_dir = ""

    @property
    def attr(self):  
        return self.__attr
    
    def __init__(self, input_dir, destination_dir):    
        self.output_dir = destination_dir     
        self.process(input_dir)
        self.__attr = input_dir    

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


    
    
        
