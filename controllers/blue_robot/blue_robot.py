from controller import Robot
import numpy as np
import cv2

TIMESTEP = 16
robot = Robot()

# Get the robot's receiver
receiver = robot.getDevice("supervisor receiver")
receiver.enable(TIMESTEP)

left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')
left_motor.setPosition(float('inf'))
left_motor.setVelocity(0.5)
right_motor.setPosition(float('inf'))
right_motor.setVelocity(0.5)


while robot.step(TIMESTEP) != -1:
    # Check if there is a new image from the Supervisor
    if receiver.getQueueLength() > 0:
        img_data = receiver.getBytes()

        img = np.frombuffer(img_data, dtype=np.uint8)
        img = np.reshape(img, (640, 640, 4))

        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        low_yellow = np.array([20, 100, 100])
        high_yellow = np.array([30, 255, 255])
        yellow_mask = cv2.inRange(img, low_yellow, high_yellow)

        low_blue = np.array([90, 200, 100])
        high_blue = np.array([120, 255, 255]) 
        blue_mask = cv2.inRange(img, low_blue, high_blue)

        low_red = np.array([160, 100, 100])
        high_red = np.array([180, 255, 255])
        red_mask = cv2.inRange(img, low_red, high_red)

        combined_mask = yellow_mask + blue_mask + red_mask

        img = cv2.bitwise_and(img, img, mask=combined_mask)
        img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)

        receiver.nextPacket()

        cv2.imshow('Image from Player', img)
        cv2.waitKey(1)

    
