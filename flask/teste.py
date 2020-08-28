#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 09:28:35 2020

@author: jonnyteronni
"""
import os, sys
sys.path.append(os.path.abspath("../"))
from Face_recognition import face_recon


# from Plot_graphs import plot_bars
# from from_sql_processing import stats


pwd_SQL = "root"

face_recon('Speaker_small.mp4',pwd_SQL)
# stats(pwd_SQL)
