import cv2
import os

def jpg_to_single_frame_mp4(image_path, output_file):
    # Check if the image file exists
    if not os.path.isfile(image_path):
        print(f"Error: The file {image_path} does not exist.")
        return

    # Read the image
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Error: Unable to read the image {image_path}.")
        return

    height, width, layers = frame.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_file, fourcc, 1, (width, height))

    # Write the single frame
    video.write(frame)

    # Release the VideoWriter
    video.release()

    print(f"Single-frame video saved as {output_file}")

def extract_first_digit(s):
    if s and s[0].isdigit():
        return int(s[0])
    return None

if __name__ == '__main__':
    # Example usage
    image_path = "snapshots/0_2024-09-07_16-01-54-304.jpg"
    output_file = "output_video.mp4"
    jpg_to_single_frame_mp4(image_path, output_file)