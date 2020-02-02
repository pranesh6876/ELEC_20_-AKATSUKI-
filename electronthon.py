import cv2
import math
import serial
import numpy as np
import struct
cap=cv2.VideoCapture(0)
file=open("coordinates.txt","+a")

ser = serial.Serial()
ser.baudrate = 250000#the baud rate over which the arduino and python will communicate
ser.port = 'COM23' # change it for your owm com port
ser.open()
kernel = np.ones((7,7),np.uint8)
def nothing(x):
	pass
def calibrateColor(color, def_range):   # this function sets the color of the object that you want to detect
    global kernel
    name = 'Calibrate ' + color
    cv2.namedWindow(name)
    cv2.createTrackbar('Hue', name, def_range[0][0] + 20, 180,nothing)
    cv2.createTrackbar('Sat', name, def_range[0][1], 255,nothing)
    cv2.createTrackbar('Val', name, def_range[0][2], 255,nothing)
    while (1):
        ret, frameinv = cap.read(0)
        frame = cv2.flip(frameinv, 1)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        hue = cv2.getTrackbarPos('Hue', name)
        sat = cv2.getTrackbarPos('Sat', name)
        val = cv2.getTrackbarPos('Val', name)

        lower = np.array([hue - 20, sat, val])
        upper = np.array([hue + 20, 255, 255])

        mask = cv2.inRange(hsv, lower, upper)
        dilated = cv2.dilate(mask, kernel, iterations=1)
        cv2.imshow(name, dilated)           #the values are 180,20,240 in white background

        k = cv2.waitKey(5) & 0xFF
        if k == ord(' '):
            cv2.destroyWindow(name)
            return np.array([[hue - 20, sat, val], [hue + 20, 255, 255]])
        elif k == ord('d'):
            cv2.destroyWindow(name)
            return def_range
red_range = np.array([[158,85,72],[180,255,255]])
red_range = calibrateColor('red', red_range)
while(1):
    print("new loop")
    Ready=0     #Ready signal for Laptop
    _,img=cap.read()
    img=cv2.flip(img,1)#to get a flipped image
    height,width,depth=img.shape
   #img=cv2.resize(img,(height*3,int(width*1.1)))
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    kernal = np.ones((5, 5), "uint8")
    mask = cv2.inRange(hsv, red_range[0], red_range[1])
    mask = cv2.dilate(mask, kernel, iterations=1)
    while Ready==0:
        ser.write('1'.encode())    #ready signal for arduino is sent
        Ready=ser.read()
    print("ready received from arduino")
    angle=0
    temp=0
    while temp==0:
        temp=ser.read()
    print("angle keyword received")
    angle=ser.readline()
    angle=int(angle)
    print(angle)
    file.write(str(angle))
    for i in range(height):
        for j in range(width):
            if mask[i,j]==255:
                file.write(','+str(i))#now change the scaling factor and create a csv file
                file.write(','+str(j))
    file.write('\n')
    cv2.imshow('Color Tracking',img)
    if angle==200:
        break
ser.close()
cv2.destroyAllWindows()