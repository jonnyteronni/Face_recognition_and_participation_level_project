#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 09:28:35 2020

@author: jonnyteronni
"""
import os, sys
sys.path.append(os.path.abspath("../"))
from Face_recognition_NEW_JI import face_recon
from Plot_graphs import plot_bars

face_recon('small.mp4',"tasmania")
# plot_bars()