import nibabel as nib
import numpy as np
import os

# Function to create a thresholded MIP image along the X-axis
def create_thresholded_mip_x(input_path, output_dir, threshold):
    # Load the NIfTI image
    img = nib.load(input_path)
    data = img.get_fdata()

    # Create an empty MIP image with the same dimensions as the input
    mip_image_x = np.zeros_like(data.max(axis=0))

    # Generate the MIP image by taking the maximum intensity along the X-axis
    for x in range(data.shape[0]):
        mip_image_x = np.maximum(mip_image_x, data[x, :, :])

    # Apply thresholding to the MIP image
    thresholded_mip_image_x = np.where(mip_image_x >= threshold, mip_image_x, 0)

    # Ensure that the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generate the output file name with the threshold value for the X-axis
    threshold_str = str(threshold).replace(".", "_")  # Convert float to string and replace decimal point
    output_file_x = os.path.join(output_dir, f"thresholded_MIP_X_{threshold_str}.nii.gz")

    # Create a new NIfTI image for the thresholded MIP data along the X-axis
    mip_nifti_x = nib.Nifti1Image(thresholded_mip_image_x, img.affine)

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


if __name__ == "__main__":
    # Replace these paths with your input and output directory paths
    input_file = "/home/ubuntu/RSNA/dataset/output_directory/10127/1554/ct_scan.nii.gz"
    output_dir = "/home/ubuntu/RSNA/mip_experimentations/"

    if os.path.exists(input_file):
        # Prompt the user for the threshold value
        threshold = float(input("Enter the threshold value: "))

        # Call the functions for each axis to create and save the thresholded MIP images
        output_file_x = create_thresholded_mip_x(input_file, output_dir, threshold)
        print(f"Thresholded MIP image along X-axis saved to {output_file_x}")

        output_file_y = create_thresholded_mip_y(input_file, output_dir, threshold)
        print(f"Thresholded MIP image along Y-axis saved to {output_file_y}")

        output_file_z = create_thresholded_mip_z(input_file, output_dir, threshold)
        print(f"Thresholded MIP image along Z-axis saved to {output_file_z}")

    else:
        print(f"Input file '{input_file}' not found.")