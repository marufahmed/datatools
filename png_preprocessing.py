import os
import numpy as np
import cv2
import pandas as pd
import multiprocessing

# Function to resize a 2D image to the desired size with interpolation
def resize_image(image, target_size=(128, 128)):
    return cv2.resize(image, target_size, interpolation=cv2.INTER_LINEAR)

# Create a 3D volume by dynamically sampling slices
def create_3d_volume_with_keyframes(images, target_size=(128, 128, 128)):
    n_slices = len(images)
    
    keyframe_indices = np.linspace(0, n_slices - 1, target_size[2], dtype=int)
    
    selected_slices = []
    for idx in keyframe_indices:
        selected_slices.append(images[idx])
    
    resized_slices = [resize_image(slice_array, target_size[:2]) for slice_array in selected_slices]
    volume = np.stack(resized_slices, axis=-1)
    
    return volume

# Function to create the desired output directory structure
def create_output_directories(output_dir, patient_id, scan_id):
    patient_dir = os.path.join(output_dir, patient_id)
    scan_dir = os.path.join(patient_dir, scan_id)
    
    os.makedirs(scan_dir, exist_ok=True)
    
    return scan_dir

# Function to save the three projected images along each axis as separate PNG files
def save_projected_images(volume, output_dir):
    # Project along X axis
    for i in range(volume.shape[0]):
        cv2.imwrite(os.path.join(output_dir, f'projection_x_{i}.png'), volume[i, :, :])
    # Project along Y axis
    for i in range(volume.shape[1]):
        cv2.imwrite(os.path.join(output_dir, f'projection_y_{i}.png'), volume[:, i, :])
    # Project along Z axis
    for i in range(volume.shape[2]):
        cv2.imwrite(os.path.join(output_dir, f'projection_z_{i}.png'), volume[:, :, i])

# Example usage for the input directory
input_dir = '/path/to/png_files_directory'
output_dir = '/path/to/output_directory'

# Specify X, Y, and Z dimensions for the 3D volume
x_size, y_size, z_size = 128, 128, 128

# Traverse the entire input directory
for patient_id in os.listdir(input_dir):
    patient_dir = os.path.join(input_dir, patient_id)
    
    if os.path.isdir(patient_dir):
        for scan_id in os.listdir(patient_dir):
            scan_dir = os.path.join(patient_dir, scan_id)
            
            if os.path.isdir(scan_dir):
                print(f"Processing patient {patient_id}, scan {scan_id}...")
                
                # List all PNG files in the current scan directory
                png_images = load_and_sort_png_files(scan_dir)
                
                if len(png_images) > 0:
                    print("Creating 3D volume...")
                    output_volume = create_3d_volume_with_keyframes(png_images, (x_size, y_size, z_size))
                    
                    # Create the output directory for the current scan
                    output_scan_dir = create_output_directories(output_dir, patient_id, scan_id)
                    
                    print("Saving the projected images...")
                    save_projected_images(output_volume, output_scan_dir)
                    
                    print(f"Projected images saved in '{output_scan_dir}'.")
                else:
                    print("No PNG files found in the current scan directory.")
