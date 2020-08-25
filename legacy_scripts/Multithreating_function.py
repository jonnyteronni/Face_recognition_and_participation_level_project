# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 17:36:19 2020

@author: BlackTemplario
"""

import face_recognition
def face_encoding_f(frame, face_locations,num_jitters, model):
    return face_recognition.face_encodings(frame, face_locations,num_jitters, model)
   