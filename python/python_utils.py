import cv2
import os
import numpy as np
from glob import glob

def jpg_to_mp4(image_folder, output_file, fps=30):
    # Get list of jpg files in the folder
    images = sorted(glob(os.path.join(image_folder, "*.jpg")))
    
    if not images:
        print("No JPG images found in the specified folder.")
        return
    
    # Read the first image to get dimensions
    frame = cv2.imread(images[0])
    height, width, layers = frame.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    # Write each image to the video
    for image in images:
        frame = cv2.imread(image)
        video.write(frame)

    # Release the VideoWriter
    video.release()

    print(f"Video saved as {output_file}")

if __name__ == '__main__':
    # Example usage
    image_folder = "path/to/your/image/folder"
    output_file = "output_video.mp4"
    jpg_to_mp4(image_folder, output_file)