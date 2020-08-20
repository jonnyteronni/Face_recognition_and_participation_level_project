#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 22:19:06 2020

@author: jonnyteronni
"""

import os, sys
import cv2

webcam = cv2.VideoCapture(0)



if not webcam.isOpened():
        print("Could not open webcam")
        sys.exit()

name = input("What is your name?\n").replace(' ','_')

if not os.path.exists(f'datasets/{name}'):
    os.makedirs(f'datasets/{name}')



number=1
while os.path.isfile(f'datasets/{name}/{number}.jpg'):
    number +=1
    print(number)
    
exit_number=number+30
while webcam.isOpened():
    
    status, printscreen = webcam.read()
    if not status:
        print("Could not read frame")
        sys.exit()
    
    
    if (number-exit_number) !=0:
        cv2.imwrite(f'datasets/{name}/{number}.jpg',printscreen)
        number +=1

        
    
    cv2.imshow('OpenCV', printscreen) 
    
    # press "Q" to stop
    if cv2.waitKey(1) & 0xFF == ord('q'):

        cv2.destroyAllWindows() 
        break
print(number)    
# Release resources
printscreen.release()
cv2.destroyAllWindows() 