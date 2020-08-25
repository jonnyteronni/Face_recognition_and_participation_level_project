
# import necessary packages
import cvlib as cv
import cv2
from mss import mss
import numpy
import multiprocessing
# from PIL import ImageGrab
# from vidgear.gears import ScreenGear

sct = mss()
monitor = None
webcam = None

# choose between webcam('w'), part of screen_part('sp'), fullscreen('fs') or video('v')
type_of_input = 'sp'


if type_of_input == 'w':
    # with webcam
    webcam = cv2.VideoCapture(0)
    if not webcam.isOpened():
        print("Could not open webcam")
        exit()
    
elif type_of_input == 'sp':
    # with screen_part
    monitor = {"top": 40, "left": 0, "width": 1300, "height": 1000}
elif type_of_input == 'fs':
    # with fullscreen
    monitor = sct.monitors[1]
elif type_of_input =='v':
    # with video
    webcam = cv2.VideoCapture('gallery.mp4')


ash= 8
printscreen=None

# Multiprocessing

# def detected_multi(printscreen):
#     face, confidence = cv.detect_face(printscreen)
#     return face, confidence
    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     executor.map(detected_multi,(type_of_input,webcam))
    #     # detected_multi(type_of_input,webcam)
        
    #     # press "Q" to stop
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         cv2.destroyAllWindows() 
    #         break
   
queue_from_cam = multiprocessing.Queue()

def cam_loop(queue_from_cam,webcam):
    # print 'initializing cam'
    # cap = cv2.VideoCapture(0)
    # print 'querying frame'
    # hello, img = cap.read()
    

    
    
    # print 'queueing image'
    queue_from_cam.put(printscreen)
    # print 'cam_loop done'

cam_process = multiprocessing.Process(target=cam_loop,args=(queue_from_cam,webcam,))
cam_process.start()

while True:
    
    if type_of_input == 'w' or type_of_input=='v':
        status, printscreen = webcam.read()
        if not status:
            print("Could not read frame")
            exit()

    elif type_of_input=='sp' or type_of_input=='fs':
        webcam = numpy.array(sct.grab(monitor))
        gray = cv2.cvtColor(webcam, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray,(ash-1,ash))
        printscreen = numpy.delete(webcam, numpy.s_[-1], 2)
    
    
    
    while queue_from_cam.empty():
        pass
    
    # while True:
        
    
        
    
    # Using PIL
    # printscreen =  numpy.array(ImageGrab.grab(bbox=(0,40,1000,800)))
    
    # apply face detection
    face, confidence = cv.detect_face(printscreen)
    
    print(face)
    print(confidence)
    
    # loop through detected faces
    for idx, f in enumerate(face):
        
        (startX, startY) = f[0], f[1]
        (endX, endY) = f[2], f[3]
    
        # draw rectangle over face
        cv2.rectangle(printscreen, (startX,startY), (endX,endY), (0,255,0), 2)
    
        text = "{:.2f}%".format(confidence[idx] * 100)
    
        Y = startY - 10 if startY - 10 > 10 else startY + 10
    
        # write confidence percentage on top of face rectangle
        cv2.putText(printscreen, text, (startX,Y), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (0,255,0), 2)
    
    # display output
    cv2.imshow("Real-time face detection", printscreen)
    
    # press "Q" to stop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows() 
        break
    
# release resources
printscreen.release()
cv2.destroyAllWindows()  