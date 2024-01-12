#PREPROCESS
import os
import numpy as np
import cv2
import nibabel as nib
import pydicom
import pandas as pd
import multiprocessing
from tqdm import tqdm
import time 
import matplotlib.pyplot as plt


# Function to create a combined 2D image along the X-axis
def create_combined_image_x(input_volume):
    combined_image_x = np.max(input_volume, axis=0)  # Combine along the X-axis
    return combined_image_x

# Function to create a combined 2D image along the Y-axis
def create_combined_image_y(input_volume):
    combined_image_y = np.max(input_volume, axis=1)  # Combine along the Y-axis
    return combined_image_y

# Function to create a combined 2D image along the Z-axis
def create_combined_image_z(input_volume):
    combined_image_z = np.max(input_volume, axis=2)  # Combine along the Z-axis
    return combined_image_z
# Function to save a 2D image as JPEG
def save_jpeg(image, output_path):
    plt.imshow(image, cmap='gray')
    plt.axis('off')
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    plt.close()

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

# Example usage for the input directory and Parquet file
input_dir = '/path_to/train_images'
output_dir = '/path_to/rsna_preprocessing_output'
parquet_file = '/path_to/train_dicom_tags.parquet'

# Specify X, Y, and Z dimensions for the 3D volume
x_size, y_size, z_size = 128, 128, 128

# Load Parquet metadata
print("Loading Parquet metadata...")
parquet_metadata = load_parquet_metadata(parquet_file)

# Function to count the number of scan directories
def count_scan_directories(root_dir):
    scan_count = 0
    for patient_id in os.listdir(root_dir):
        patient_dir = os.path.join(root_dir, patient_id)
        if os.path.isdir(patient_dir):
            for scan_id in os.listdir(patient_dir):
                scan_dir = os.path.join(patient_dir, scan_id)
                if os.path.isdir(scan_dir):
                    scan_count += 1
    return scan_count

# Calculate the total number of scans in the dataset
total_scans = count_scan_directories(input_dir)

# ... (previous code)

# Initialize counters for processed scans and processed DICOM images
processed_scans = 0
processed_images = 0

# Initialize the start time
start_time = time.time()

# Initialize a set to store processed scan IDs
processed_scan_ids = set()

# Function to extract scan ID from log lines
def extract_scan_id(line):
    try:
        parts = line.split()
        if len(parts) >= 11 and parts[9] == "Processing" and parts[10] == "patient":
            patient_index = parts.index("patient") + 1  # Index of patient ID (follows "patient")
            scan_index = parts.index("scan") + 1  # Index of scan ID (follows "scan")
            
            patient_id = int(parts[patient_index].strip(','))
            scan_id = int(parts[scan_index].strip('...'))
            
            return patient_id, scan_id
    except:
        pass
    return None




# Calculate the total number of scans in the dataset
total_scans = count_scan_directories(input_dir)



# Function to create a thresholded MIP image along the X-axis
def create_thresholded_mip_x(input_volume, output_dir, threshold):
    # Create an empty MIP image with the same dimensions as the input
    mip_image_x = np.zeros_like(input_volume.max(axis=0))

    # Generate the MIP image by taking the maximum intensity along the X-axis
    for x in range(input_volume.shape[0]):
        mip_image_x = np.maximum(mip_image_x, input_volume[x, :, :])

    # Apply thresholding to the MIP image
    thresholded_mip_image_x = np.where(mip_image_x >= threshold, mip_image_x, 0)

    # Ensure that the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generate the output file name with the threshold value for the X-axis
    threshold_str = str(threshold).replace(".", "_")  # Convert float to string and replace decimal point
    output_file_x = os.path.join(output_dir, f"thresholded_MIP_X_{threshold_str}.nii.gz")

    # Create a new NIfTI image for the thresholded MIP data along the X-axis
    mip_nifti_x = nib.Nifti1Image(thresholded_mip_image_x, np.diag(voxel_spacing + [1.0]))

    # Save the thresholded MIP image to the specified output path
    nib.save(mip_nifti_x, output_file_x)
    return output_file_x

# Function to create a thresholded MIP image along the Y-axis
def create_thresholded_mip_y(input_path, output_dir, threshold):
    # Load the NIfTI image
    img = nib.load(input_path)
    data = img.get_fdata()

    # Create an empty MIP image with the same dimensions as the input
    mip_image_y = np.zeros_like(data.max(axis=1))

    # Generate the MIP image by taking the maximum intensity along the Y-axis
    for y in range(data.shape[1]):
        mip_image_y = np.maximum(mip_image_y, data[:, y, :])

    # Apply thresholding to the MIP image
    thresholded_mip_image_y = np.where(mip_image_y >= threshold, mip_image_y, 0)

    # Generate the output file name with the threshold value for the Y-axis
    threshold_str = str(threshold).replace(".", "_")  # Convert float to string and replace decimal point
    output_file_y = os.path.join(output_dir, f"thresholded_MIP_Y_{threshold_str}.nii.gz")

    # Create a new NIfTI image for the thresholded MIP data along the Y-axis
    mip_nifti_y = nib.Nifti1Image(thresholded_mip_image_y, img.affine)

    # Save the thresholded MIP image to the specified output path
    nib.save(mip_nifti_y, output_file_y)
    return output_file_y

# Function to create a thresholded MIP image along the Z-axis
def create_thresholded_mip_z(input_path, output_dir, threshold):
    # Load the NIfTI image
    img = nib.load(input_path)
    data = img.get_fdata()

    # Create an empty MIP image with the same dimensions as the input
    mip_image_z = np.zeros_like(data.max(axis=2))

    # Generate the MIP image by taking the maximum intensity along the Z-axis
    for z in range(data.shape[2]):
        mip_image_z = np.maximum(mip_image_z, data[:, :, z])

    # Apply thresholding to the MIP image
    thresholded_mip_image_z = np.where(mip_image_z >= threshold, mip_image_z, 0)

    # Generate the output file name with the threshold value for the Z-axis
    threshold_str = str(threshold).replace(".", "_")  # Convert float to string and replace decimal point
    output_file_z = os.path.join(output_dir, f"thresholded_MIP_Z_{threshold_str}.nii.gz")

    # Create a new NIfTI image for the thresholded MIP data along the Z-axis
    mip_nifti_z = nib.Nifti1Image(thresholded_mip_image_z, img.affine)

    # Save the thresholded MIP image to the specified output path
    nib.save(mip_nifti_z, output_file_z)
    return output_file_z

# Specify the threshold value for MIP images
threshold = 1000  # You can adjust this threshold as needed

# Traverse the entire input directory and skip scans that are already processed
for patient_id in os.listdir(input_dir):
    patient_dir = os.path.join(input_dir, patient_id)

    if os.path.isdir(patient_dir):
        for scan_id in os.listdir(patient_dir):
            scan_dir = os.path.join(patient_dir, scan_id)

            if os.path.isdir(scan_dir):
                if (int(patient_id), int(scan_id)) in processed_scan_ids:
                    print(f"Scan {scan_id} for patient {patient_id} has already been processed. Skipping...")
                    continue  # Skip processing if the scan is in the processed_scan_ids set

                output_scan_dir = create_output_directories(output_dir, patient_id, scan_id)
                output_file = os.path.join(output_scan_dir, 'ct_scan.nii.gz')

                print(f"Processing patient {patient_id}, scan {scan_id}...")

                # List all DICOM files in the current scan directory
                dicom_images = load_and_sort_dicom_files(scan_dir)

                if len(dicom_images) > 0:
                    processed_images += len(dicom_images)

                    print(f"Creating 3D volume for {len(dicom_images)} DICOM images...")

                    # Initialize the output_volume variable
                    output_volume, voxel_spacing, selected_filenames = create_3d_volume_with_keyframes(
                        dicom_images, (x_size, y_size, z_size), parquet_data=parquet_metadata)

                    # Update the counters for processed scans
                    processed_scans += 1

                    print("Saving the 3D volume...")
                    nifti_image = nib.Nifti1Image(output_volume, np.diag(voxel_spacing + [1.0]))
                    nib.save(nifti_image, output_file)

                    print(f"Combined and resampled image saved as '{output_file}'.")

                    # Create combined 2D images along X, Y, and Z axes
                    combined_image_x = create_combined_image_x(output_volume)
                    combined_image_y = create_combined_image_y(output_volume)
                    combined_image_z = create_combined_image_z(output_volume)

                    # Save the combined images
                    plt.imsave(os.path.join(output_scan_dir, "combined_image_x.jpg"), combined_image_x, cmap="gray")
                    plt.imsave(os.path.join(output_scan_dir, "combined_image_y.jpg"), combined_image_y, cmap="gray")
                    plt.imsave(os.path.join(output_scan_dir, "combined_image_z.jpg"), combined_image_z, cmap="gray")

                else:
                    print("No DICOM files found in the current scan directory.")
