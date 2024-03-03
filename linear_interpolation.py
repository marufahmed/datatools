import os
import numpy as np
import cv2
import nibabel as nib
import pydicom
import pandas as pd
import multiprocessing

# Function to resize a 2D image to the desired size with interpolation
def resize_image(image, target_size=(128, 128)):
    return cv2.resize(image, target_size, interpolation=cv2.INTER_LINEAR)

# Define default values for slice thickness and pixel spacing
default_slice_thickness = 1.0
default_pixel_spacing_x = 1.0
default_pixel_spacing_y = 1.0

# Create a 3D volume by dynamically sampling slices
def create_3d_volume_with_keyframes(images, target_size=(128, 128, 128), parquet_data=None):
    n_slices = len(images)
    
    keyframe_indices = np.linspace(0, n_slices - 1, target_size[2], dtype=int)
    
    selected_slices = []
    selected_filenames = []

    for idx in keyframe_indices:
        selected_slices.append(images[idx]["pixel_array"])
        selected_filenames.append(images[idx]["filename"])
    
    slice_thicknesses = []
    pixel_spacings = []
    for filename in selected_filenames:
        matching_row = parquet_data[parquet_data['path'] == filename]
        if not matching_row.empty:
            slice_thicknesses.append(matching_row['SliceThickness'].values[0])
            pixel_spacings.append([matching_row['PixelSpacingX'].values[0], matching_row['PixelSpacingY'].values[0]])
        else:
            slice_thicknesses.append(default_slice_thickness)
            pixel_spacings.append([default_pixel_spacing_x, default_pixel_spacing_y])
    
    resized_slices = [resize_image(slice_array, target_size[:2]) for slice_array in selected_slices]
    volume = np.stack(resized_slices, axis=-1)
    
    voxel_spacing = [
        pixel_spacings[0][0],
        pixel_spacings[0][1],
        slice_thicknesses[0]
    ]
    
    return volume, voxel_spacing, selected_filenames

# Function to load and sort DICOM files from a directory numerically
def load_and_sort_dicom_files(patient_dir):
    dicom_files = [os.path.join(root, file) for root, dirs, files in os.walk(patient_dir) for file in files if file.endswith('.dcm')]
    
    # Create a list to store DICOM images as dictionaries
    dicom_images = []
    
    for full_path in dicom_files:
        dicom_data = pydicom.dcmread(full_path)
        
        filename = f"{int(dicom_data.SeriesNumber)}_{int(dicom_data.InstanceNumber):04d}.nii.gz"
        pixel_array = dicom_data.pixel_array
        
        # Create a dictionary for each DICOM image
        dicom_image = {
            "filename": filename,
            "pixel_array": pixel_array,
        }
        
        dicom_images.append(dicom_image)
    
    # Sort the DICOM images by their slice positions
    dicom_images.sort(key=lambda x: x["filename"])
    
    return dicom_images

# Function to load Parquet metadata from a file
def load_parquet_metadata(parquet_file):
    return pd.read_parquet(parquet_file)

# Function to create the desired output directory structure
def create_output_directories(output_dir, patient_id, scan_id):
    patient_dir = os.path.join(output_dir, patient_id)
    scan_dir = os.path.join(patient_dir, scan_id)
    
    os.makedirs(scan_dir, exist_ok=True)
    
    return scan_dir
def resize_3d_volume(volume, target_size=(128, 128, 128)):
    current_size = volume.shape
    x_scale = target_size[0] / current_size[0]
    y_scale = target_size[1] / current_size[1]
    z_scale = target_size[2] / current_size[2]

    # Use trilinear interpolation for upsampling
    interpolation = cv2.INTER_LINEAR if (x_scale > 1.0 or y_scale > 1.0 or z_scale > 1.0) else cv2.INTER_AREA

    resized_volume = np.zeros(target_size)
    for z in range(target_size[2]):
        z_orig = int(z / z_scale)
        z_frac = z / z_scale - z_orig
        for y in range(target_size[1]):
            y_orig = int(y / y_scale)
            y_frac = y / y_scale - y_orig
            for x in range(target_size[0]):
                x_orig = int(x / x_scale)
                x_frac = x / x_scale - x_orig

                # Trilinear interpolation
                value = (1 - z_frac) * ((1 - y_frac) * ((1 - x_frac) * volume[x_orig, y_orig, z_orig] + x_frac * volume[x_orig + 1, y_orig, z_orig])
                                        + y_frac * ((1 - x_frac) * volume[x_orig, y_orig + 1, z_orig] + x_frac * volume[x_orig + 1, y_orig + 1, z_orig]))
                + z_frac * ((1 - y_frac) * ((1 - x_frac) * volume[x_orig, y_orig, z_orig + 1] + x_frac * volume[x_orig + 1, y_orig, z_orig + 1])
                            + y_frac * ((1 - x_frac) * volume[x_orig, y_orig + 1, z_orig + 1] + x_frac * volume[x_orig + 1, y_orig + 1, z_orig + 1]))

                resized_volume[x, y, z] = value

    return resized_volume

# Example usage for the input directory and Parquet file
input_dir = '/kaggle/input/rsna-2023-abdominal-trauma-detection/train_images'
output_dir = '/kaggle/working/output_directory'
parquet_file = '/kaggle/input/rsna-2023-abdominal-trauma-detection/train_dicom_tags.parquet'

# Specify X, Y, and Z dimensions for the 3D volume
x_size, y_size, z_size = 128, 128, 128

# Load Parquet metadata
print("Loading Parquet metadata...")
parquet_metadata = load_parquet_metadata(parquet_file)

# Traverse the entire input directory
for patient_id in os.listdir(input_dir):
    patient_dir = os.path.join(input_dir, patient_id)
    
    if os.path.isdir(patient_dir):
        for scan_id in os.listdir(patient_dir):
            scan_dir = os.path.join(patient_dir, scan_id)
            
            if os.path.isdir(scan_dir):
                print(f"Processing patient {patient_id}, scan {scan_id}...")
                
                # List all DICOM files in the current scan directory
                dicom_images = load_and_sort_dicom_files(scan_dir)
                
                if len(dicom_images) > 0:
                    output_scan_dir = create_output_directories(output_dir, patient_id, scan_id)

                    print("Creating 3D volume...")
                    output_volume, voxel_spacing, selected_filenames = create_3d_volume_with_keyframes(
                        dicom_images, (x_size, y_size, z_size), parquet_data=parquet_metadata)

                    # Upsample or downsample the volume to the desired size
                    output_volume = resize_3d_volume(output_volume, target_size=(128, 128, 128))

                    print("Saving the 3D volume...")
                    nifti_image = nib.Nifti1Image(output_volume, np.diag(voxel_spacing + [1.0]))
                    output_file = os.path.join(output_scan_dir, 'ct_scan.nii.gz')
                    nib.save(nifti_image, output_file)
                    print(f"Combined and resized image saved as '{output_file}'.")
                
            else:
                print("No DICOM files found in the current scan directory.")
                
