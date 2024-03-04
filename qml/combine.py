# This script is used to create one image from three axis wise projected images
from PIL import Image

def combine_images(image_x_path, image_y_path, image_z_path, output_path):
    # Open the grayscale images
    image_x = Image.open(image_x_path)
    image_y = Image.open(image_y_path)
    image_z = Image.open(image_z_path)
    
    # Ensure images have the same size
    width, height = image_x.size
    assert (width, height) == image_y.size == image_z.size, "Images must have the same size"
    
    # Create a new RGB image
    combined_image = Image.new("RGB", (width, height))
    
    # Iterate over each pixel and set RGB values
    for y in range(height):
        for x in range(width):
            # Get pixel values from each image
            pixel_x = image_x.getpixel((x, y))[0]
            pixel_y = image_y.getpixel((x, y))[0]
            pixel_z = image_z.getpixel((x, y))[0]
            
            # Create RGB tuple
            rgb_pixel = (pixel_x, pixel_y, pixel_z)
            
            # Set RGB value in combined image
            combined_image.putpixel((x, y), rgb_pixel)
    
    # Save the combined image
    combined_image.save(output_path)
    print(f"Combined image saved at {output_path}")


# Example usage
combine_images("19-14374-combined_image_x.jpg", "19-14374-combined_image_y.jpg", "19-14374-combined_image_z.jpg", "19-14374-combined_rgb_image.jpg")
