#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 02:15:27 2020

@author: jonnyteronni
"""
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


#Creating timeseries to export to sql
# enter your server IP address/domain name
HOST = "35.192.100.10" # or "domain.com"
# database name, if you want just to connect to MySQL server, leave it empty
DATABASE = "timeseries"
# this is the user you create
USER = "antero"
# user password
PASSWORD = "root"
# connect to MySQL server


# Connect to localhost

cnx = mysql.connector.connect(user = 'root', password = "tKaNblvrQipO1!",host = 'localhost',
                          database = 'project9')


# #Checking and create video_id (called frame id in SQL)
# cnx = mysql.connector.connect(user = USER, password = "root",host = HOST,
#                           database = DATABASE)
try:
    cnx.is_connected()
    print("Connection open")
    cursor = cnx.cursor()
    query = ("SELECT * FROM timeseries;")
    cursor.execute(query)
    results = cursor.fetchall()

except print("Connection is not successfully open"):
    pass

timeseries_df=pd.DataFrame(results,columns=["frame_id","name","time","record_source","date"])


timeseries_Aula_df = timeseries_df[timeseries_df['frame_id']==10].copy()

timeseries_Aula_df['frame_id']=21


timeseries_Aula_df.drop('date',axis=1,inplace=True)

# create sqlalchemy engine
engine = create_engine("mysql+pymysql://{user}:{pw}@35.192.100.10/{db}"
                       .format(user='antero',
                               pw='root',
                               db='timeseries'))

timeseries_Aula_df.to_sql('timeseries', con = engine, if_exists = "append",index=False)

print("Exported to SQL")