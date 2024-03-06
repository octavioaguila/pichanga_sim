from controller import Robot
import numpy as np
import cv2
from PIL import Image

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

    img = img.reshape((720, 1280, 3))
    img = img[:, :, :3]
    
    # Convert the image to the HSV color space
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    low_yellow = np.array([20, 100, 100])
    high_yellow = np.array([30, 255, 255])
    yellow_mask = cv2.inRange(img_hsv, low_yellow, high_yellow)
    low_blue = np.array([110, 200, 100])
    high_blue = np.array([120, 255, 255]) 
    blue_mask = cv2.inRange(img_hsv, low_blue, high_blue)
    
    #Ignoring my own goal
    blue_mask[0:720, 0:106] = 0


    low_red = np.array([160, 100, 100])
    high_red = np.array([180, 255, 255])
    red_mask = cv2.inRange(img_hsv, low_red, high_red)

    yellow_mask_ = Image.fromarray(yellow_mask)
    blue_mask_ = Image.fromarray(blue_mask)
    red_mask_ = Image.fromarray(red_mask)

    bbox_detected = []
    bbox_detected.append(["yellow", yellow_mask_.getbbox()])
    bbox_detected.append(["blue", blue_mask_.getbbox()])
    bbox_detected.append(["red", red_mask_.getbbox()])
    
    # Combine masks
    combined_mask = yellow_mask + blue_mask + red_mask
    
    # Apply the mask to the original BGR image
    img_masked = cv2.bitwise_and(img, img, mask=combined_mask)

    for bbox in bbox_detected:
        if bbox[1] is not None:
            x1, y1, x2, y2 = bbox[1]
            cv2.rectangle(img_masked, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img_masked, bbox[0], (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

    

    cv2.imshow('Blue Robot', img_masked)
    cv2.waitKey(1)

