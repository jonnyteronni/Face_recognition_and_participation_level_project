import os, sys
from flask import Flask, render_template, redirect,  request, Response, stream_with_context, send_from_directory, url_for, session
sys.path.append(os.path.abspath("../"))
from Encode_images_for_face_recognition_byfilename import encode_images
from Face_recognition import face_recon
from from_sql_processing import stats
import pandas as pd
import cv2



app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


app.secret_key = "secret key"

@app.route("/")
def index():
    return render_template("home/welcome.html")

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
            # pwd_SQL = 'tasmania'
            
            # Face recognition script
            file_name = session.get('FILE_NAME',pwd_SQL)
            face_recon(file_name,pwd_SQL)
            print('Face recognition done')
            
            
            # Import to SQL
            
            
            
            
            stats(pwd_SQL)
            
            
            return render_template("home/face_recognition.html")
        
        
        elif 'show_video' in request.form:
            video = '/static/video/final.mp4'
            
            df = pd.DataFrame({'name': ['Somu', 'Kiku', 'Amol', 'Lini'],
                        'physics': [68, 74, 77, 78],
                        'chemistry': [84, 56, 73, 69],
                        'algebra': [78, 88, 82, 87]})
            
            facetime_bar_gif='/static/gif/facetime_bar.gif'
            return render_template("home/face_recognition.html", videos = video,tables=[df.to_html(classes='table table-hover')], titles=df.columns.values, facetime_bar_gif = facetime_bar_gif)    
        
    else:
    
        return render_template("home/face_recognition.html")


@app.route("/ui-tables")
def tables():
    
    df = pd.DataFrame({'name': ['Somu', 'Kiku', 'Amol', 'Lini'],
                        'physics': [68, 74, 77, 78],
                        'chemistry': [84, 56, 73, 69],
                        'algebra': [78, 88, 82, 87]})
    
       
    return render_template("home/ui-tables.html",tables=[df.to_html(classes='table table-hover')], titles=df.columns.values)


    
# @app.route("/upload", methods=['POST','GET'])
# def upload_video():
#     if request.method == 'POST':
#         # Video
#         if 'video_form' in request.form:
#             target = os.path.join(APP_ROOT, 'static/video')
        
#             if not os.path.isdir(target):
#                 os.mkdir(target)
        
#             for file in request.files.getlist("video"):
#                 FILE_NAME = file.filename
#                 # FILE_NAME = "input.mp4"
#                 destination = "/".join([target, FILE_NAME])
#                 file.save(destination)
            
#             return render_template("upload.html")
        
        
#         elif 'images_form' in request.form:
#             target = os.path.join(APP_ROOT, 'static/images')
        
#             if not os.path.isdir(target):
#                 os.mkdir(target)
        
#             for file in request.files.getlist("images"):
#                 FILE_NAME = file.filename
#                 destination = "/".join([target, FILE_NAME])
#                 file.save(destination)
#             return render_template("upload.html")

        
#         elif 'run_model' in request.form:
#             # Model to encode images
#             encode_images()
#             print('Images encoded')

#             # Face recognition script
#             exec(open("../Face_recognition.py").read())
#             print('Face recognition done')
            
#             return render_template("upload.html")
        
#         elif 'show_video' in request.form:
#             video = '/static/video/final.mp4'
            
#             return render_template("upload.html", videos = video)        
       
        
#     else:
#         return render_template("upload.html")



    



# @app.route('/video', methods = ['POST','GET'])
# # def open_video():
# #     return render_template("video_test.html")
# def send_file():
#     # return render_template('video_test.html',filename = 'VIDEO_UPLOAD/output.mp4')
#     return send_from_directory("VIDEO_UPLOAD", filename = 'output.mp4')
# bootstrap = Bootstrap(app)

if __name__ == "__main__":
    app.run(port=4555, debug=True)