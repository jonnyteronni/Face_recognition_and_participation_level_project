import os, sys
from flask import Flask, render_template, redirect,  request, Response, stream_with_context, send_from_directory, url_for, session
sys.path.append(os.path.abspath("../"))
from Encode_images_for_face_recognition_byfilename import encode_images
from Face_recognition import face_recon
from from_sql_processing import stats
from Plot_graphs import plot_bars
import pandas as pd
import cv2

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))



app.secret_key = "secret key"

@app.route("/")
def index():
    return render_template("home/welcome.html")


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r



@app.route("/ui-upload_data",methods=['POST','GET'])
def upload_video():
    if request.method == 'POST':
        # Video
        if 'video_form' in request.form:
            target = os.path.join(APP_ROOT, 'static/video')
        
            if not os.path.isdir(target):
                os.mkdir(target)
        
            for file in request.files.getlist("video"):

                FILE_NAME = file.filename
                             
                session['FILE_NAME'] = str(FILE_NAME)

                destination = "/".join([target, FILE_NAME])
                file.save(destination)
            
            return render_template("home/ui-upload_data.html")
        
        
        elif 'images_form' in request.form:
            target = os.path.join(APP_ROOT, 'static/images')
        
            if not os.path.isdir(target):
                os.mkdir(target)
        
            for file in request.files.getlist("images"):
                FILE_NAME = file.filename
                destination = "/".join([target, FILE_NAME])
                file.save(destination)
            return render_template("home/ui-upload_data.html")

    
   
    
    else:
        return render_template("home/ui-upload_data.html")
    

@app.route("/face_recognition",methods=['POST','GET'])
def face_models():

    if request.method == 'POST':
        
        if 'run_model' in request.form:
            # Model to encode images
            encode_images()
            print('Images encoded')
            
            
            # SQL Password
            pwd_SQL = "tKaNblvrQipO1!"

            
            # Face recognition script
            file_name = session.get('FILE_NAME')
            fps = face_recon(file_name,pwd_SQL)
            session['FPS'] = str(fps)
            print('Face recognition done')
            
            model_finished = "Model has finished running"                 
                      
            
            return render_template("home/face_recognition.html",model_finished=model_finished)
        
        
        elif 'show_video' in request.form:
                       
            try:
                # SQL Password
                pwd_SQL = "tKaNblvrQipO1!"
                session['SQL_PASSWORD'] = str(pwd_SQL)
                
    
                fps = float(session.get('FPS'))
                total_video_length, upload_date,unique_speakers_identified,video_name,length_each_frame, final_stats_df, timeseries_df,df_raw_data = stats(pwd_SQL)
                
    
                
                video = f'/static/video/final_{video_name}'
                facetime_bar_gif=f'/static/gif/bar_graph_{video_name}'

                
                return render_template("home/face_recognition.html", \
                                       videos = video,tables=[final_stats_df.to_html(classes='table table-hover')],\
                                       facetime_bar_gif = facetime_bar_gif, \
                                       total_video_length = total_video_length,\
                                       upload_date = upload_date,\
                                       unique_speakers_identified = unique_speakers_identified,\
                                       video_name = video_name)
            except TypeError as err:
                print(err)
                return render_template("home/face_recognition.html")
        
    else:
    
        return render_template("home/face_recognition.html")


@app.route("/ui-tables")
def tables():


    pwd_SQL = session.get('SQL_PASSWORD')
    
    df_raw_data = stats(pwd_SQL)[7]
    
    
    #Filters and datacleaning
    df_raw_data=df_raw_data[df_raw_data['frame_id']!=21]
    df_raw_data=df_raw_data[df_raw_data['name']!='Unknown']
    df_raw_data['time'] = df_raw_data['time'].round(2)
    df_raw_data['Video_id'] = df_raw_data['frame_id']
    df_raw_data.drop('frame_id', axis = 1, inplace=True)
    
    
    
    
    df_raw_data = df_raw_data[['Video_id','name','time','record_source','date']]
    df_group_data = df_raw_data.groupby(by=['Video_id','name','record_source','date']).sum()


    return render_template("home/ui-tables.html",tables=[df_group_data.to_html(classes='table table-hover')])

@app.route("/stats")
def stats_function():
    
    return render_template("home/stats.html")

  


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000)#, debug=True)