# from the video each frame converted into image and stored in the local system for creating dataset for training

import cv2
import os

# Common directory to store all the video folders
common_output_folder = 'Attendence_Dataset'
os.makedirs(common_output_folder, exist_ok=True)

video_files = [
    '/content/AKSHAY.MOV',
    '/content/DIVAS.MOV',
    '/content/JUNAID.MOV'
]

for video_file in video_files:
    # Create a folder for each video
    video_name = os.path.splitext(video_file)[0]
    video_output_folder = os.path.join(common_output_folder, video_name)
    os.makedirs(video_output_folder, exist_ok=True)

    
    video_path = os.path.join('video_folder', video_file)  
    cap = cv2.VideoCapture(video_path)

    frame_count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1

        
        frame_filename = os.path.join(video_output_folder, f'frame_{frame_count:04d}.jpg')
        cv2.imwrite(frame_filename, frame)

    cap.release()
    cv2.destroyAllWindows()

    print(f"Extracted {frame_count} frames from '{video_file}' and saved them in '{video_output_folder}'")

print(f"All frames are saved in the common directory: '{common_output_folder}'")