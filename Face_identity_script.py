
# It helps in identifying the faces 
import cv2, sys, numpy, os 
import time
from mss import mss
from PIL import Image
# from mtcnn.mtcnn import MTCNN

size = 4
face_cascade  = 'haarcascades/haarcascade_frontalface_alt2.xml'
eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')
left_eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_lefteye_2splits.xml')
datasets = 'datasets'
  
# Part 1: Create fisherRecognizer 
print('Recognizing Face Please Be in sufficient Lights...') 
  
# Create a list of images and a list of corresponding names 
(images, lables, names, id) = ([], [], {}, 0) 
for (subdirs, dirs, files) in os.walk(datasets): 
    for subdir in dirs: 
        names[id] = subdir 
        subjectpath = os.path.join(datasets, subdir) 
        for filename in os.listdir(subjectpath): 
            path = subjectpath + '/' + filename 
            lable = id
            images.append(cv2.imread(path, 0)) 
            lables.append(int(lable)) 
        id += 1
(width, height) = (200, 200) 
  
# Create a Numpy array from the two lists above 
(images, lables) = [numpy.array(lis) for lis in [images, lables]] 
  
# OpenCV trains a model from the images 
# NOTE FOR OpenCV2: remove '.face' 
model = cv2.face.LBPHFaceRecognizer_create() 
model.train(images, lables) 
  

# Part 2: Use fisherRecognizer on screen (was on camera stream) 
face_cascade = cv2.CascadeClassifier(face_cascade ) 
# webcam = cv2.VideoCapture(0)
sct = mss()
monitor = {"top": 40, "left": 0, "width": 1000, "height": 640}
while True: 
    
    # Give screen to opencv
    
    # last_time = time.time()

    # Get raw pixels from the screen, save it to a Numpy array

    # For part of screen
    img = numpy.array(sct.grab(monitor))

    # Display the picture in grayscale
    # cv2.imshow('OpenCV/Numpy grayscale',
    #            cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))

    # print("fps: {}".format(1 / (time.time() - last_time)))
    
          
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # detectMultiScale:
    # img
    # scaleFactor: Parameter specifying how much the image size is reduced at each image scale.
    # minNeighbors: Parameter specifying how many neighbors each candidate rectangle should have to retain it

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces: 
        # cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2) 
        face = gray[y:y + h, x:x + w]
        # roi_color = img[y:y+h, x:x+w]
        # eyes = eye_cascade.detectMultiScale(face)
        # l_eye = left_eye_cascade.detectMultiScale(face)
        face_resize = cv2.resize(face, (width, height)) 
        # Try to recognize the face 
        prediction = model.predict(face_resize) 
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3) 
        # for (ex,ey,ew,eh) in eyes:
            # cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),3)
        # for (ex,ey,ew,eh) in l_eye:
        #     cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(100,255,0),1)
        
       
        if prediction[1]<500: 
  
           cv2.putText(img, '% s - %.0f' % 
(names[prediction[0]], prediction[1]), (x-10, y-10),  
cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0)) 
        else: 
          cv2.putText(img, 'not recognized',  
(x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0)) 
    
    # Display the picture
    cv2.imshow("OpenCV/Numpy normal", img)
    
    # cv2.imshow('OpenCV', im) 
      
     # Press "q" to quit
    if cv2.waitKey(25) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break