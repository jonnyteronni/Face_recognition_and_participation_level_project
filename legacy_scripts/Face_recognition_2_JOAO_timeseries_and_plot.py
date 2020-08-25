import face_recognition
import cv2
import numpy as np
from mss import mss
import sys
import os
import time

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
#video_capture = cv2.VideoCapture(0)




# choose between webcam('w'), part of screen_part('sp'), fullscreen('fs') or video('v')

# -------DASHBOARD--------
type_of_input = 'fs'

# hog for cpu, cnn for GPU
MODEL_LOCATION = 'hog'

# large or small. Small is faster but less accurate
MODEL_ENCODING = 'small'

# How many times to re-sample the face when calculating encoding. Higher is more accurate, but slower (i.e. 100 is 100x slower)
# Only integers
NUM_JITTERS_ENCODING = 1

# How much distance between faces to consider it a match. Lower is more strict. 0.6 is typical best performance.
TOLERANCE_RECOGNITION = 0.6

# Resize of 
# resize_value = 1

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
time_count["break_time"]=0
initial_total = time.time()

none_counter=0

#Timeseries
#timeseries=[["start",0]]
timeseries=[]

while True:
    # Grab a single frame of video
    # ret, frame = video_capture.read()
    
    initial_frame = time.time()
    name="none"
    
    print("beginning while",name)

    if type_of_input == 'w' or type_of_input=='v':
        ret, frame = webcam.read()
        if not ret:
            print("Could not read frame")
            sys.exit()

    elif type_of_input=='sp' or type_of_input=='fs':
        webcam = np.array(sct.grab(monitor))
        # gray = cv2.cvtColor(webcam, cv2.COLOR_BGR2GRAY)
        # gray = cv2.resize(gray,(ash-1,ash))
        frame = np.delete(webcam, np.s_[-1], 2)

    # Frame from RGB to Gray
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)    

    # Resize frame of video to 1/4 size for faster face recognition processing
    # small_frame = cv2.resize(frame, (0, 0), fx=1, fy=1)
    small_frame = frame
    
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame,model = MODEL_LOCATION)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations,num_jitters = NUM_JITTERS_ENCODING, model = MODEL_ENCODING)
        
        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_faces, face_encoding, tolerance=TOLERANCE_RECOGNITION)
            name = "Unknown"
            none_counter=0

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_faces, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_names[best_match_index]
                none_counter=0
                

            face_names.append(name)
            
    # process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        # top *= 1
        # right *= 1
        # bottom *= 1
        # left *= 1

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Smile you are on camera!!!', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
    
    # Print FPSq
    print(1/(time.time() - initial_frame))
    
    # Facetime measures to time dictionary
    if (str(name) in time_count.keys()) & (none_counter<4): # Change here the number of frames we want to facetime
        time_ite=time_count[name]+(time.time() - initial_frame)
        time_count[name]=time_ite
        # timeseries
        timeseries.append([name,(time.time() - initial_frame)])
    elif (none_counter>=5):
        time_ite=time_count["break_time"]+(time.time() - initial_frame)
        time_count["break_time"]=time_ite
        # timeseries  
        timeseries.append(["break_time",time.time() - initial_frame])
    else:
        time_ite=(time.time() - initial_frame)
        time_count[name]=time_ite
         # timeseries      
        timeseries.append([name,time_ite])
        
    print("end while",name)
    print("none counter",none_counter)
    none_counter+=1


        
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


# Release handle to the webcam
if type_of_input == 'w':
    webcam.release()
cv2.destroyAllWindows()



#Creating timeseries dataframe and cum sum
import pandas as pd
timeseries_df=pd.DataFrame(timeseries)
for i in timeseries_df[0].unique():
    timeseries_df[i]=timeseries_df[timeseries_df[0]==i][1]
    timeseries_df[i].fillna(0,inplace=True)
    timeseries_df[i]=timeseries_df[i].cumsum()

#timeseries_df.drop([1],axis=1,inplace=True)


#Ploting timeseries of facetime
import matplotlib.pyplot as plt 
import numpy as np
import imageio
import os


order=timeseries_df.max()[1:].sort_values(ascending=False).keys().tolist()
y_pos=np.arange(len(order))
x_speak=[]
ims=0

for i in timeseries_df.iterrows():
    for ii in np.arange(len(order)):
        x_speak.append(i[1][(order[ii])])
    plt.figure(figsize=(15,2))
    plt.barh(y_pos, x_speak, align='center',color="slategrey")
    plt.yticks(y_pos,order)
    plt.xlim(xmax=int(1.05*max(timeseries_df.max()[1:].values)))
    
    x_speak=[]
    ims+=1
    
#Saving the frames
    plt.savefig('./gif/all/'+str(ims)+'.png',dpi=150)
    plt.show()
    

#Creating Gif
folder = './gif/all' 
files = [f"{folder}\\{file}" for file in os.listdir(folder)]

images = [imageio.imread(file) for file in files]
imageio.mimwrite('./gif/movie.gif', images, fps=5)


# int(webcam.get(cv2.CAP_PROP_FPS)
    # Parameters for saving
    # ---------------------
    # loop : int
    #     The number of iterations. Default 0 (meaning loop indefinitely).
    # duration : {float, list}
    #     The duration (in seconds) of each frame. Either specify one value
    #     that is used for all frames, or one value for each frame.
    #     Note that in the GIF format the duration/delay is expressed in
    #     hundredths of a second, which limits the precision of the duration.
    # fps : float
    #     The number of frames per second. If duration is not given, the
    #     duration for each frame is set to 1/fps. Default 10.
    # palettesize : int
    #     The number of colors to quantize the image to. Is rounded to
    #     the nearest power of two. Default 256.
    # subrectangles : bool
    #     If True, will try and optimize the GIF by storing only the
    #     rectangular parts of each frame that change with respect to the
    #     previous. Default False.

