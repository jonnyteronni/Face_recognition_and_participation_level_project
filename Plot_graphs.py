

#Ploting timeseries of facetime
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os
import glob
import math
import cv2
from pylab import rcParams
import random

def plots(timeseries_df):
    color_set=(['thistle', 'bisque', 'moccasin', 'khaki', 'silver', 
               'darkgrey', 'palegreen', 'darkseagreen', 'powderblue', 'skyblue', 'mediumturquoise', 
               'mediumaquamarine', 'lightseagreen', 'dodgerblue', 'cadetblue', 'slateblue', 
               'mediumblue', 'darkblue'])
    random.shuffle(color_set)
    
    
    timeseries_df2=timeseries_df.copy()
    time_cumsum=timeseries_df2.pop("time").cumsum()
    timeseries_df2.pop("name")
    timeseries_df2.pop("record_source")
    timeseries_df2.pop("date")
    timeseries_df2.pop("frame_id")
    try:
        timeseries_df2.pop('Unknown')
    except KeyError :
        pass
    try:
        timeseries_df2.pop('break_time')
    except KeyError :
        pass
    
    
    totals=timeseries_df2.max().sort_values(ascending=False)
    height1=4    
    if totals.shape[0]>3:
        height1=height1+(totals.shape[0]-3)*0.25
    
    #rcParams['figure.figsize'] = 15, height1
    rcParams['figure.dpi'] =300
    rcParams['savefig.dpi'] = 300
    
    rcParams['font.size'] = 14
    
    rcParams['axes.spines.right'] = False
    rcParams['axes.spines.top'] = False
    rcParams['axes.spines.bottom'] = True
    
    rcParams['axes.facecolor'] = '#202940'
    rcParams['axes.edgecolor'] = 'white'
    rcParams['axes.labelcolor'] = 'white'
    rcParams['axes.xmargin'] = 0.02
    rcParams['axes.ymargin'] = 0.02
    
    rcParams['ytick.color'] = "white"
    rcParams['xtick.color'] = "white"
    
    rcParams['legend.edgecolor'] = "white"
    rcParams['legend.edgecolor'] = "#202940"
    rcParams['legend.labelspacing'] = 0.75
    
    
    plt.clf() 
    colorss=[]
    plt.figure(figsize=(15,height1))
    for i in totals.index:
        
        colorss.append(color_set.pop())
        plt.plot(time_cumsum, timeseries_df2[i],linewidth=2.5,color=colorss[-1],label=i)
    
    plt.xlim(0,time_cumsum.max()*1.05)
    plt.ylim(0,timeseries_df2.max().max()*1.05)
        
    # plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left',labelcolor='w')
    
    patchList = []
    for index,key in enumerate(totals.index):
            data_key = mpatches.Patch(color=colorss[index], label=key)
            patchList.append(data_key)
    
    plt.legend(handles=patchList,bbox_to_anchor=(1.0, 1.0), loc='upper left',labelcolor='w')
    
    plt.ylabel('Facetime cumsum (s)')
    plt.xlabel('Timestep (s)')
    plt.tight_layout()
    plt.savefig("static/plot/lineplot.png", facecolor='#202940')
    plt.clf()

    
    
    
    # Bar plot:
    height2=1.5   
    if totals.shape[0]>2:
        height2=height2+(totals.shape[0]-2)*0.30
      
    #rcParams['figure.figsize'] = 15, height2
    plt.figure(figsize=(15,height2))
    plt.barh(timeseries_df2.max().sort_values(ascending=True).index, timeseries_df2.max().sort_values(ascending=True), align='center',color=colorss[::-1])
    plt.xlim(xmax=math.ceil(1.05*max(timeseries_df2.max().values)))
    plt.xlabel('Facetime total (s)')
    plt.tight_layout()
        # plt.xlabel(label)
        
   
    plt.savefig("static/plot/barplot.png", facecolor='#202940')

    
    print("Line and barplot printed")




def plot_bars_video(timeseries_df,length_each_frame,video_name):
    timeseries_df2=timeseries_df.copy()
    timeseries_df2.pop("name")
    timeseries_df2.pop("record_source")
    timeseries_df2.pop("date")
    timeseries_df2.pop("frame_id")

    # if max(timeseries_df2.max()) > 120:
    #     timeseries_df2=timeseries_df2[timeseries_df2.columns]/60
    #     label='speaker (minutes)'
    # else:
    label='speaker (seconds)'

    try:
        timeseries_df2.pop('break_time')
    except KeyError :
        pass
    try:
        timeseries_df2.pop('none')
    except KeyError :
        pass

    order=timeseries_df2.max().sort_values(ascending=False).keys().tolist() #####


    y_pos=np.arange(len(order))
    x_speak=[]
    ims=0
    imss=[]


    color=['darkblue', 'mediumblue', 'slateblue', 'cadetblue', 'dodgerblue',
           "lightseagreen","mediumaquamarine", "mediumturquoise", "skyblue",
           "powderblue","darkseagreen", "palegreen", "darkgrey","silver","gainsboro",
           "khaki", "moccasin","bisque","thistle"]


    files = glob.glob('static/plot/all/*')
    for f in files:
        os.remove(f)


    for i in timeseries_df.iterrows():
        for ii in np.arange(len(order)):
            x_speak.append(i[1][(order[ii])])
        plt.figure(figsize=(15,3.5))
        plt.barh(y_pos, x_speak, align='center',color=color)
        plt.yticks(y_pos,order)
        plt.xlim(xmax=math.ceil(1.05*max(timeseries_df2.max().values)))
        plt.xlabel(label)
        # plt.annotate(str(round(time_cumsum[[i][0][0]],1)),+"/"+str(round(time_cumsum,1).max()), (0.5,0.5),color="b",backgroundcolor="w",size=12)
        # print(str(round(time_cumsum[[i][0][0]],1))+"/"+str(round(time_cumsum,1).max()))


        x_speak=[]
        ims+=1
        imss.append(ims)

    #Saving the frames
        plt.savefig('static/plot/all/'+str(ims)+'.png')  #dpi=150
        # plt.show()


    save_id=str(np.random.randint(100)) #########################
    frame_width=1080 # frame_width = int(webcam.get(3)) #########
    frame_height=216# frame_height = int(webcam.get(4)) #################
    fps=1/length_each_frame


    # Codec
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

    out = cv2.VideoWriter('static/plot/output_temp'+save_id+'.mp4',fourcc, fps, (frame_width,frame_height))
    for frame in imss:#np.arange(1,imss+1,1):
        path='static/plot/all/'+str(frame)+".png"

        frame2=cv2.imread(path,flags=cv2.IMREAD_COLOR)
        # print(frame2)
        # frame2 = cv2.imread(path,cv2.IMREAD_UNCHANGED)[:,:,-1]

        out.write(frame2)

    out.release()
    # os.system("ffmpeg -i static/gif/facetime_bar"+save_id+".mp4 -vcodec libx264 static/gif/facetime_bar"+save_id+".mp4 -y")

    files = glob.glob('./static/plot/all/*')
    for f in files:
        os.remove(f)

    print("Plot bar video saved")



    # #Alternative way of Creating Gif
    # folder = 'static/gif/all'
    # files = [f"{folder}/{file}.png" for file in (imss)]


    # images = [imageio.imread(file) for file in files]
    # imageio.mimwrite('static/gif/facetime_bar.gif', images, fps=1/length_each_frame)

    # print("GIF saved")

    # files = glob.glob('../gif/all/*')
    # for f in files:
    #     os.remove(f)
