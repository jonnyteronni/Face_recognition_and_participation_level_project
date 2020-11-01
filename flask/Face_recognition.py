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
import mysql.connector
import imageio




def face_recon(FILE_NAME,pwd_SQL):

    # Check the running OS to import mss

    if platform.system() == 'Linux':
        print('Yeiii Linux is running here!')
        from mss.linux import MSS as mss
    else:
        print('Recommend using linux to run this script.')
        from mss import mss


    # choose between webcam('w'), part of screen_part('sp'), fullscreen('fs') or video('v')

    # -------DASHBOARD--------

    type_of_input = 'v'


    video_input= 'static/video/'+str(FILE_NAME)
    # video_input= 'static/video/small.mp4'  ###########################
    # # SQL Password
    # pwd_SQL = "tKaNblvrQipO1!"
    # pwd_SQL = 'tasmania'


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

    # sct=mss()


    if type_of_input == 'w':
        # with webcam
        webcam = cv2.VideoCapture(0)
        if not webcam.isOpened():
            print("Could not open webcam")
            sys.exit()

    elif type_of_input == 'sp':
        # with screen_part
        sct=mss()
        monitor = {"top": 200, "left": 0, "width": 1000, "height": 500}
    elif type_of_input == 'fs':
        # with fullscreen
        sct=mss()
        monitor = sct.monitors[2]
    elif type_of_input =='v':
        # with video
        webcam = cv2.VideoCapture(video_input)





    # Get image information
    known_faces = []
    known_names= []
    # FILE_NAME = "input.mp4"

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

    # Time counts for facetime

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





        #Length of video, total of frames and length of each frame



    if (type_of_input == 'w') | (type_of_input == 'v'):

        frame_width = int(webcam.get(3))
        frame_height = int(webcam.get(4))
        fps = webcam.get(cv2.CAP_PROP_FPS)
        length_each_frame = 1/fps




    elif (type_of_input=='sp') | (type_of_input=='fs'):
        frame_width = monitor['width']
        frame_height = monitor['height']
        fps=30


    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    out = cv2.VideoWriter('static/video/output_temp.mp4',fourcc, fps , (frame_width,frame_height))



    # Loop Begin -----------------------------------------------------------------

    while True:

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

            frame = np.delete(webcam, np.s_[-1], 2)

        frame_count+=1


        small_frame = cv2.resize(frame, (0, 0), fx=RESIZE_FRAME_PERC, fy=RESIZE_FRAME_PERC)


        rgb_small_frame = small_frame


        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame,model = MODEL_LOCATION)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations,num_jitters = NUM_JITTERS_ENCODING, model = MODEL_ENCODING)


        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_faces, face_encoding, tolerance=TOLERANCE_RECOGNITION)
            name = "Unknown"


            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_faces, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_names[best_match_index]
                none_counter=0




            face_names.append(name)



        # Facetime measures to time dictionary


        none_counter_limit=3 # Change here the number of frames we want to facetime for the break time
        for i in face_names:
            if (none_counter<none_counter_limit) & (len(face_names)>0) :
                timeseries.append([i,1/len(face_names)])


        # Print FPSThere's no excuse not to do what makes you happy.
        print(1/(time.time() - initial_frame))


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
        out.write(frame)

        # Display the resulting image
        if type_of_input != 'v':
          cv2.imshow('Smile you are on camera!!!', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # if 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


        # Facetime breaktime to time dictionary
        none_counter_limit=3 # Change here the number of frames we want to facetime for the breakt time
        if (none_counter>=none_counter_limit):
            timeseries.append(["break_time",1])

        none_counter+=1


        # Print FPS

        fps_counter= 1/(time.time() - initial_frame)
        print(fps_counter)
    # Loop end -----------------------------------------------------------------

    # Print facetime stats
    print("Total", (time.time() - initial_total))


    cv2.destroyAllWindows()
    # define variables for output video

    if type_of_input == 'w' or type_of_input=='v':
    #     # frame size of webcam or video
    #     frame_width = int(webcam.get(3))
    #     frame_height = int(webcam.get(4))

    #     # fps = int(webcam.get(cv2.CAP_PROP_FPS))
        webcam.release()


    if type_of_input=='sp' or type_of_input=='fs':
        length_video=(time.time() - initial_total)
        total_frames=frame_count
        length_each_frame=length_video/total_frames


    # Release handle to the webcam
    
    if type_of_input!='v':
        FILE_NAME = 'LIVE.mp4'


    out.release()
    os.system(f"ffmpeg -i static/video/output_temp.mp4 -vcodec libx264 static/video/final_{FILE_NAME} -y")


    print("Video file processed")





    #Creating timeseries to export to sql
    # enter your server IP address/domain name
    HOST = "face-recognition-ecs2.cdvhsbdbaawd.eu-west-2.rds.amazonaws.com" 
    # database name, if you want just to connect to MySQL server, leave it empty
    DATABASE = "face_recognition_ecs2_db"
    # this is the user you create
    USER = "jonnyteronni"
    # user password
    PASSWORD = "pdiSrJDNHccN"
    # connect to MySQL server


    timeseries_sql=pd.DataFrame(timeseries,columns=["name","time"])

    timeseries_sql["time"]=timeseries_sql["time"]*length_each_frame

    source={"w":"webcam/LIVE.mp4","sp":"screen_part/LIVE.mp4","fs":"fullscreen/LIVE.mp4", "v":str("video"+"_"+video_input)}
    timeseries_sql["record_source"]=source[type_of_input]

    #Checking and create video_id (called frame id in SQL)
    cnx = mysql.connector.connect(user = USER, password = PASSWORD, host = HOST,
                              database = DATABASE)
    try:
        cnx.is_connected()
        print("Connection open")
        cursor = cnx.cursor()
        query = ("SELECT * FROM timeseries;")
        cursor.execute(query)
        results = cursor.fetchall()

    except print("Connection is not successfully open"):
        pass

    timeseries_df=pd.DataFrame(results,columns=["id","frame_id","name","time","record_source","date"])

    if timeseries_df["frame_id"].max() > 0:
        timeseries_sql["frame_id"]=(timeseries_df["frame_id"].max()+1)
    else:
        timeseries_sql["frame_id"]=1


    timeseries_sql=timeseries_sql[['frame_id','name', 'time', 'record_source']]

    # create sqlalchemy engine
    engine = create_engine("mysql+pymysql://{user}:{pw}@face-recognition-ecs2.cdvhsbdbaawd.eu-west-2.rds.amazonaws.com/{db}"
                            .format(user=USER,
                                    pw=PASSWORD,
                                    db=DATABASE))

    timeseries_sql.to_sql('timeseries', con = engine, if_exists = "append",index=False)

    print("Exported to SQL")


    return fps
