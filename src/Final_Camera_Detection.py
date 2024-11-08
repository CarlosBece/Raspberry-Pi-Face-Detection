# Final_Camera_Detection.py
import cv2
import subprocess
import os
import numpy as np
from collections import deque

# Load the Haar cascade library for face detection (pre-trained model)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Initialize the camera to capture video feed
cap = cv2.VideoCapture(0)

# Set thresholds for detection
left_threshold = 100  # Threshold to determine if the target is on the left
right_threshold = 100  # Threshold to determine if the target is on the right
center_threshold = 50  # Threshold for determining if the target is centered
similarity_threshold = 5000  # Threshold for matching target face with detected face

# Define path for saving and loading the target face image
TARGET_FACE_PATH = 'target_face.jpg'
target_face = None  # Variable to hold the target face image
face_saved = False  # Flag to check if the target face is saved

# Initialize a queue to hold the positions of detected faces for smoothing
position_queue = deque(maxlen=5)

# Start the motor control program in a separate subprocess
motor_process = subprocess.Popen(["./Final_Motor_Move"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Function to save the target face to a file
def save_target_face(face_image):
    cv2.imwrite(TARGET_FACE_PATH, face_image)  # Save the image to the defined path
    print("Target face saved.")

# Function to load the saved target face from file
def load_target_face():
    if os.path.exists(TARGET_FACE_PATH):  # Check if the target face file exists
        return cv2.imread(TARGET_FACE_PATH, cv2.IMREAD_GRAYSCALE)  # Load the saved face in grayscale
    return None  # Return None if no saved face is found

# Load the previously saved target face if available
target_face = load_target_face()
if target_face is not None:
    face_saved = True  # Mark face as saved if it exists

try:
    # Main loop for capturing frames and detecting faces
    while True:
        ret, frame = cap.read()  # Capture a frame from the camera
        if not ret:
            print("Failed to grab frame.")
            break  # Exit the loop if frame capture fails

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert the captured frame to grayscale
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)  # Detect faces in the frame

        # Define the frame center for comparison
        frame_height, frame_width = frame.shape[:2]
        frame_center_x = frame_width // 2  # X-coordinate of the center of the frame

        best_match_value = float('inf')  # Variable to store the best match value for face comparison
        best_match_index = -1  # Index to store the best matching face

        # Loop through detected faces and compare each with the target face
        for i, (x, y, w, h) in enumerate(faces):
            detected_face = gray_frame[y:y + h, x:x + w]  # Crop the detected face from the frame

            if not face_saved:
                # Save the first detected face as the target face
                save_target_face(detected_face)
                target_face = detected_face
                face_saved = True

            if face_saved and target_face is not None:
                # Resize the detected face to match the target face size
                detected_face_resized = cv2.resize(detected_face, (target_face.shape[1], target_face.shape[0]))

                # Calculate similarity (match value) between the target face and the detected face
                match_value = cv2.norm(target_face, detected_face_resized, cv2.NORM_L2)

                # Update the best match if the current match value is better (lower)
                if match_value < best_match_value and match_value < similarity_threshold:
                    best_match_value = match_value
                    best_match_index = i  # Store the index of the best matching face

        # Second pass to label faces based on the best match
        for i, (x, y, w, h) in enumerate(faces):
            face_center_x = x + w // 2  # Calculate the X-coordinate of the center of the face

            if i == best_match_index:
                # Label the closest matching face as "Target"
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(frame, "Target", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                # Add the face center X position to the queue for smoothing
                position_queue.append(face_center_x)
                smoothed_center_x = int(np.mean(position_queue))  # Calculate the smoothed center

                # Motor control logic based on the smoothed face position
                if smoothed_center_x < frame_center_x - left_threshold:
                    print("Target on the left side")
                    motor_process.stdin.write("ccw\n")  # Send counterclockwise command to the motor
                    motor_process.stdin.flush()
                elif smoothed_center_x > frame_center_x + right_threshold:
                    print("Target on the right side")
                    motor_process.stdin.write("cw\n")  # Send clockwise command to the motor
                    motor_process.stdin.flush()
                elif frame_center_x - center_threshold < smoothed_center_x < frame_center_x + center_threshold:
                    print("Target centered")
                    motor_process.stdin.write("stop\n")  # Stop the motor if the target is centered
                    motor_process.stdin.flush()
            else:
                # Label all other faces as "Unknown"
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, "Unknown", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display the resulting frame with labels
        cv2.imshow('Face Detection with Motor Control', frame)

        # Break the loop on pressing 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except BrokenPipeError:
    print("Motor process terminated unexpectedly.")
finally:
    # Release resources
    cap.release()  # Release the camera
    cv2.destroyAllWindows()  # Close all OpenCV windows
    if motor_process.poll() is None:
        motor_process.terminate()  # Terminate the motor control process if it's still running
