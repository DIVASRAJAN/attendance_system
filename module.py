import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.models import load_model

model = load_model('assets/Face_rec_3.h5')


# to show live camera 
def generate_frames():

    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break

        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            
        if not ret:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    cap.release()


            

  
def classify_frame():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if success:
            frame1 = cv2.resize(frame, (224, 224))
            frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
            frame1 = np.expand_dims(frame1, axis=0)
            # frame1 = preprocess_input(frame1)

            predictions = model.predict(frame1)
            class_label = np.argmax(predictions)
            names=['akshay','divas','junaid']
            class_label = names[class_label]
            

        cap.release()
        return class_label
    



def save_Pic(name):
    import cv2
    import os

    cap = cv2.VideoCapture(0)

    output_directory = f'new_member/{name}'  
    os.makedirs(output_directory, exist_ok=True)

    frame_count = 0 

    while True:
        ret, frame = cap.read()

        if not ret:
            break  

        frame_count += 1

        frame_filename = os.path.join(output_directory, f'frame_{frame_count}.jpg')
        cv2.imwrite(frame_filename, frame)
        print(f'Saved: {frame_filename}')
        yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + open(frame_filename, 'rb').read() + b'\r\n')
        
