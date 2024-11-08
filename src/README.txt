** Camera Face Detection and Motor Control System **
	Author: Carlos Becerril Ceballos

** Overview **
The present src folder includes the necessary files to perform camera face detection by using the OpenCV library in order to achieve direction motor control based on the first detected face's position.
The present file to run are: 
1. Final_Camera_Detection.py (File to achieve camera face detection by using OpenCV)
2. Final_Motor_Move.c (File to achieve motor control movement)
3. haarcascade_frontalface_default.xml (Haar Cascades Detection library)

** Requirements **
To successfully run the present Camera Face Detection and Motor Control System, ensure that your Raspberry Pi 4 version already includes the following packages and system versions:

- Hardware - 
Raspberry Pi 4
Camera Module V2.1 

- Software -
1. OpenCV (OpenCV 4.6.0)
Install OpenCV using apt:
	sudo apt-get update
	sudo apt-get install python3-opencv

2. NumPy (Numpy 1.24.2)
Install Numpy using apt:
	sudo apt-get install python3-numpy

3. Motor Control Permissions
To enable the motor control program to be executed by subprocess. Make sure the motor control program Final_Motor_Move.c has executable permissions.
	chmod +x motorfinal

4. Camera Permissions
To enable the camera on the Raspberry Pi 4, ensure that the user pi (username) has the necessary permissions.
	sudo usermod -a -G video <username>

5. Python (Python-3.9.17)
This project was designed with Python-3.9.17 version, please ensure that your system has this version or a newer version to properly test the code.
To check and update your current version, use the following commands.
	python3 --version
	sudo apt-get update
	sudo apt-get install python3

6. ctypes (ctypes 1.1.0)
Verify ctypes for C-compatible data types and calling functions in shared libraries.
	pip install ctypes==1.1.0

7. picamera2 Package
Verify the installation of the picamera2 libary.
	sudo apt install -y python3-picamera2

8. Reboot
For installation purposes, reboot the system if necessary after every package installation or version update.
	sudo reboot

** Running Steps **
Steps to run the Camera Face Detection and Motor Control System:
- Step 0: (Set the French keyboard layout)
	pi@raspberrypi:~ $ setxkbmap fr

- Step 1: (Set the correct folder file to src)
	pi@raspberrypi:~ $ cd src

- Step 2: (Compile the Final_Motor_Move.c file to enable the Motor Control System:)
	pi@raspberrypi:~/src $ gcc Final_Motor_Move.c -o Final_Motor_Move

- Step: 3 (Run the Final_Camera_Detection.py file to enable Camera Face Detection)
	pi@raspberrypi:~/src $ sudo python3 Final_Camera_Detection.py

- Step 4: (Verify that an image named target_face.jpg was created in the src folder, representing the first detected face.)
target_face.jpg  - Image of the target face detected, saved in src folder once a face is detected for the first time.

- Step 5: (Verify that your src folder includes haarcascade_frontalface_default.xml file; without this file, the code will not run)
haarcascade_frontalface_default.xml - Haar Cascades Detection library.

- Step 6: Test the Camera Face Detection and Motor Control System and confirm the camera target tracking.

- Step 7: o change the face detected by the camera, delete the target_face.jpg file and repeat steps 2 and 3 to target a new face.
