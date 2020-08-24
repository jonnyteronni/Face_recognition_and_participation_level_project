

#Ploting timeseries of facetime
import matplotlib.pyplot as plt 
import numpy as np
import imageio
import os
import glob


def plot_graphs(timeseries_df):
    timeseries_df2=timeseries_df.copy()
    timeseries_df2.pop(1)
    try:
        timeseries_df2.pop('break_time')
    except KeyError :
        pass
    try:
        timeseries_df2.pop('none')
    except KeyError :
        pass
        
    files = glob.glob('./gif/all/*')
    for f in files:
        os.remove(f)
    
    order=timeseries_df2.max()[1:].sort_values(ascending=False).keys().tolist()
    
    
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
        
    
    # #Creating Gif
    # folder = './gif/all' 
    # files = [f"{folder}\\{file}" for file in (os.listdir(folder))]
    
    # teste=[]
    
    # # for file in os.listdir(folder): ########
    # #     print(file) ################
    
    # images = [imageio.imread(file) for file in files]
    # imageio.mimwrite('./gif/movie.gif', images, fps=1/length_each_frame)
    
    
    
    
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