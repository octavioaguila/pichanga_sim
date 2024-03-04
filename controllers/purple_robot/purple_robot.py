from controller import Robot
import numpy as np
import cv2
import os

TIMESTEP = 16
robot = Robot()

left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')
left_motor.setPosition(float('inf'))
left_motor.setVelocity(0.5)
right_motor.setPosition(float('inf'))
right_motor.setVelocity(0.5)


while robot.step(TIMESTEP) != -1:
    # Check if there is a new image from the Supervisor

    with open('../referee_supervisor/raw_files/camera_b.raw', 'rb') as f:
        raw_data = f.read()

    # Convert raw data to a NumPy array
    img = np.frombuffer(raw_data, dtype=np.uint8)

    img = img.reshape((640, 640, 3))
    img = img[:, :, :3]
    
    # Convert the image to the HSV color space
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    low_yellow = np.array([20, 100, 100])
    high_yellow = np.array([30, 255, 255])
    yellow_mask = cv2.inRange(img_hsv, low_yellow, high_yellow)

    low_cyan = np.array([90, 200, 100])
    high_cyan = np.array([110, 255, 255]) 
    cyan_mask = cv2.inRange(img_hsv, low_cyan, high_cyan)

    low_purple = np.array([150, 30, 50])
    high_purple = np.array([160, 255, 255])
    purple_mask = cv2.inRange(img_hsv, low_purple, high_purple)

    # Combine masks
    combined_mask = yellow_mask + cyan_mask + purple_mask
    # Apply the mask to the original BGR image
    img_masked = cv2.bitwise_and(img, img, mask=combined_mask)

    cv2.imshow('Purple Robot', img_masked)
    cv2.waitKey(1)
