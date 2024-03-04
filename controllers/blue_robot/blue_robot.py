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

    with open('../referee_supervisor/raw_files/camera_a.raw', 'rb') as f:
        raw_data = f.read()

    img = np.frombuffer(raw_data, dtype=np.uint8)

    img = img.reshape((640, 640, 3))
    img = img[:, :, :3]


    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    low_yellow = np.array([20, 100, 100])
    high_yellow = np.array([30, 255, 255])
    yellow_mask = cv2.inRange(img_hsv, low_yellow, high_yellow)

    low_blue = np.array([110, 200, 100])
    high_blue = np.array([130, 255, 255]) 
    blue_mask = cv2.inRange(img_hsv, low_blue, high_blue)

    low_red = np.array([160, 100, 100])
    high_red = np.array([180, 255, 255])
    red_mask = cv2.inRange(img_hsv, low_red, high_red)

    combined_mask = yellow_mask + blue_mask + red_mask

    img_masked = cv2.bitwise_and(img, img, mask=combined_mask)
    cv2.imshow('Blue Robot', img_masked)
    cv2.waitKey(1)



    
