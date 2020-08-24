import face_recognition
import cv2
import numpy as np
from mss import mss
import sys
import os
import time



# choose between webcam('w'), part of screen_part('sp'), fullscreen('fs') or video('v')

# -------DASHBOARD--------
type_of_input = 'v'

# hog for cpu, cnn for GPU
MODEL_LOCATION = 'hog'

# large or small. Small is faster but less accurate
MODEL_ENCODING = 'small'

# How many times to re-sample the face when calculating encoding. Higher is more accurate, but slower (i.e. 100 is 100x slower)
# Only integers
NUM_JITTERS_ENCODING = 1

# How much distance between faces to consider it a match. Lower is more strict. 0.6 is typical best performance.
TOLERANCE_RECOGNITION = 0.6

# Frame resizing (integers 1 to X)
RESIZE_FRAME = 3


# -------------

# Check what is the OS running

if os.name == 'Linux':
    print('Yeiii Linux is running here!')
else:
    print('Recommend using linux to run this script.')

sct=mss()    


if type_of_input == 'w':
    # with webcam
    webcam = cv2.VideoCapture(0)
    if not webcam.isOpened():
        print("Could not open webcam")
        sys.exit()
    
elif type_of_input == 'sp':
    # with screen_part
    monitor = {"top": 300, "left": 0, "width": 1000, "height": 800}
elif type_of_input == 'fs':
    # with fullscreen
    monitor = sct.monitors[2]
elif type_of_input =='v':
    # with video
    # webcam = cv2.VideoCapture('face_recognition/Zoom Meeting 2020-08-18 18-38-49.mp4')
    webcam = cv2.VideoCapture('Speaker.mp4')



# Get image information
known_faces = []
known_names= []

face_array = np.genfromtxt('models/known_faces_model.csv',delimiter=',')
name_array = np.genfromtxt('models/known_names_model.csv',delimiter=',',dtype='object')

# face and name arrays in a list format
for face in face_array:
    known_faces.append(face)

for name in name_array:
    known_names.append(str(name,encoding='ascii'))


# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

# Time counts for facetime
time_count={}
initial_total = time.time()


# Output to save video file on exit
frame_width = int(webcam.get(3))
frame_height = int(webcam.get(4))


fps = int(webcam.get(cv2.CAP_PROP_FPS))

# Codec
# fourcc = cv2.VideoWriter_fourcc(*'X264')
# fourcc = cv2.VideoWriter_fourcc(*'MP4V')
# fourcc = cv2.VideoWriter_fourcc(*'H264')
# cv2.VideoWriter_fourcc(*'XVID')
# cv2.VideoWriter_fourcc(c1, c2, c3, c4)
fourcc = cv2.VideoWriter_fourcc('M','J','P','G')

out = cv2.VideoWriter('output.mp4',fourcc, fps, (frame_width,frame_height))

# Frame resizing to integer
RESIZE_FRAME = int(RESIZE_FRAME)
RESIZE_FRAME_PERC = 1/RESIZE_FRAME


while webcam.isOpened():
    # Grab a single frame of video
    # ret, frame = video_capture.read()
    
    initial_frame = time.time()
    name="none"

    if type_of_input == 'w' or type_of_input=='v':
        ret, frame = webcam.read()
        if not ret:
            print("Could not read frame")
            # sys.exit()
            break

    elif type_of_input=='sp' or type_of_input=='fs':
        webcam = np.array(sct.grab(monitor))
        # webcam = cv2.cvtColor(webcam, cv2.COLOR_RGB2BGR)
        # webcam = cv2.resize(webcam,dsize)
        frame = np.delete(webcam, np.s_[-1], 2)

    # Frame from RGB to Gray
    # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)    

    # Resize frame of video to 1/4 size for faster face recognition processing
    # small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    # small_frame = frame
    
    small_frame = cv2.resize(frame, (0, 0), fx=RESIZE_FRAME_PERC, fy=RESIZE_FRAME_PERC)
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    # rgb_small_frame = small_frame[:, :, ::-1]
    # rgb_small_frame = small_frame
    
    rgb_small_frame = small_frame
    
    # Only process every other frame of video to save time
    # if process_this_frame:
        
        
    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame,model = MODEL_LOCATION)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations,num_jitters = NUM_JITTERS_ENCODING, model = MODEL_ENCODING)
    
    
    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_faces, face_encoding, tolerance=TOLERANCE_RECOGNITION)
        name = "Unknown"

        # # If a match was found in known_face_encodings, just use the first one.
        # if True in matches:
        #     first_match_index = matches.index(True)
        #     name = known_names[first_match_index]

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_faces, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_names[best_match_index]

        # else:
            
        #     # To count facetime for no people
        #     name="Unknown"


        face_names.append(name)
                
    # process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= RESIZE_FRAME
        right *= RESIZE_FRAME
        bottom *= RESIZE_FRAME
        left *= RESIZE_FRAME

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Save frame to output video
    out.write(frame)

    # Display the resulting image
    # if type_of_input != 'v':
    cv2.imshow('Smile you are on camera!!!', frame)
    
    
    
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
    # if 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
    
    # Print FPS
    print(1/(time.time() - initial_frame))
    
    # Facetime measures to time dictionary
    if str(name) in time_count.keys():
        time_count[name]=time_count[name]+(time.time() - initial_frame)
    else:
        time_count[name]=(time.time() - initial_frame)
        


        
        
##Split none time % to users
time_count_copy=time_count.copy() # To delete after trials
time_count_no_none=time_count.copy()
time_count_no_none.pop("none", None)
split_percentages={}
if 'none' in time_count.keys():
    for key in time_count.keys():
        percentage = time_count[key]/(sum(time_count.values())-time_count["none"])
        split_percentages[key]=percentage
    for key,perc in zip(time_count_no_none.keys(),split_percentages):
        time_count[key] += time_count['none'] * split_percentages[key]
    del(time_count['none'])


# Print facetime stats
print("Total", (time.time() - initial_total))
print("Time loss",(time.time() - initial_total)-sum(time_count.values()))
print(time_count)


# Release handle to the webcam
if type_of_input == 'w':
    webcam.release()
out.release()
cv2.destroyAllWindows()
