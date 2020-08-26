import face_recognition
import cv2
import numpy as np
import platform
from mss import mss
import sys
import os
import time
import pandas as pd
from sqlalchemy import create_engine

# Check the running OS to import mss


def face_recon(FILE_NAME):
    if platform.system() == 'Linux':
        print('Yeiii Linux is running here!')
        from mss.linux import MSS as mss
    else:
        print('Recommend using linux to run this script.')
        from mss import mss
    
    
    # choose between webcam('w'), part of screen_part('sp'), fullscreen('fs') or video('v')
    
    # -------DASHBOARD--------
    type_of_input = 'fs'
    
    video_input='./flask/static/video/'+str(FILE_NAME)
    
    # SQL Password
    # pwd = "tKaNblvrQipO1!"
    pwd = 'tasmania'
    
    
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
    RESIZE_FRAME = 4
    
    
    # -------------
    
    sct=mss()    
    
    
    if type_of_input == 'w':
        # with webcam
        webcam = cv2.VideoCapture(0)
        if not webcam.isOpened():
            print("Could not open webcam")
            sys.exit()
        
    elif type_of_input == 'sp':
        # with screen_part
        monitor = {"top": 200, "left": 0, "width": 1000, "height": 500}
    elif type_of_input == 'fs':
        # with fullscreen
        monitor = sct.monitors[2]
    elif type_of_input =='v':
        # with video
        webcam = cv2.VideoCapture(video_input)
    
    
    
    
    # Get image information
    known_faces = []
    known_names= []
    # FILE_NAME = "input.mp4"
    #####################################################################################
    face_array = np.genfromtxt('../models/known_faces_model.csv',delimiter=',') 
    name_array = np.genfromtxt('../models/known_names_model.csv',delimiter=',',dtype='object')
    
    # face and name arrays in a list format
    for face in face_array:
        known_faces.append(face)
    
    for name in name_array:
        known_names.append(str(name,encoding='ascii'))
    
    
    
    # Frame resizing to integer
    RESIZE_FRAME = int(RESIZE_FRAME)
    RESIZE_FRAME_PERC = 1/RESIZE_FRAME
    
    # Time counts for facetimeq
    
    initial_total = time.time()
    none_counter=0
    
    #Timeseries
    timeseries=[]
    
    #Frame count
    frame_count=0
    
    
    # Initialize some variables
    face_locations = []
    face_encodings = []# FILE_NAME = "input.mp4"
    face_names = []
    # process_this_frame = True
    
    
    frame_list = []
    
    # while webcam.isOpened():
    while True:
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
            
        frame_count+=1
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
                none_counter=0
    
    
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
            cv2.rectangle(frame, (left, bottom + 20), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom + 15), font, 0.5, (255, 255, 255), 1)
    
        # Save frame to output video
        # out.write(frame)
    
        frame_list.append(frame)
        
        # Display the resulting image
        # if type_of_input != 'v':
        cv2.imshow('Smile you are on camera!!!', frame) ######################################################################################################
        
        
        
        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
        # if 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        
        # Print FPS
        print(1/(time.time() - initial_frame))
        
            # Facetime measures to time dictionary
        none_counter_limit=3 # Change here the number of frames we want to facetime for the breakt time
        if (none_counter>=none_counter_limit):
            timeseries.append(["break_time",1])
        else:
            timeseries.append([name,1])
        
        none_counter+=1
        
    
    
    
    
    # Print facetime stats
    print("Total", (time.time() - initial_total))
    
    
    # Release handle to the webcam
    if type_of_input == 'w':
        webcam.release()
    
    cv2.destroyAllWindows()
    
    
    #Length of video, total of frames and length of each frame
    
    if (type_of_input == 'w') | (type_of_input == 'v'):
        length_video=webcam.get(cv2.CAP_PROP_POS_MSEC)/1000 #seconds
        # total_frames=webcam.get(cv2.CAP_PROP_FRAME_COUNT)
        total_frames=frame_count
        length_each_frame=length_video/total_frames
    elif (type_of_input=='sp') | (type_of_input=='fs'):
        length_video=(time.time() - initial_total)
        total_frames=frame_count
        length_each_frame=length_video/total_frames
    
    
    
    # define variables for output video
    
    if type_of_input == 'w' or type_of_input=='v':
        # frame size of webcam or video
        frame_width = int(webcam.get(3))
        frame_height = int(webcam.get(4))
         
        fps = int(webcam.get(cv2.CAP_PROP_FPS))
     
       
        
    elif type_of_input=='sp' or type_of_input=='fs':
        # frame size of webcam or video
        frame_width = monitor['width']
        frame_height = monitor['height']
        
        
        fps = 1/length_each_frame
        
        
    
    # Codec
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    
    
    # Output file
    out = cv2.VideoWriter('static/video/output_temp.mp4',fourcc, fps , (frame_width,frame_height))
    for frame in frame_list:
        out.write(frame)
    
    out.release()
    os.system("ffmpeg -i static/video/output_temp.mp4 -vcodec libx264 static/video/final.mp4 -y")
    
    
    
    
    #Creating timeseries to export to sql
    timeseries_sql=pd.DataFrame(timeseries,columns=["name","time"])
    
    timeseries_sql["time"]=timeseries_sql["time"]*length_each_frame
    
    source={"w":"webcam","sp":"screen_part","fs":"fullscreen", "v":str("video"+"_"+video_input)}
    timeseries_sql["record_source"]=source[type_of_input]

    
    
    # create sqlalchemy engine
    engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                           .format(user="root",
                                   pw=pwd,
                                   db="project9"))
    
    timeseries_sql.to_sql('timeseries', con = engine, if_exists = "append",index=False)
    
    print("Exported to SQL")
    
    return



