
import os, sys
import mysql.connector
import pandas as pd
sys.path.append(os.path.abspath("../"))
# from Plot_graphs import plot_bars


def stats(pwd_SQL):
    cnx = mysql.connector.connect(user = 'antero', password = 'root',host ='35.192.100.10',
                                  database = 'timeseries')
    
    # #TO DELETE EXISTING ENTRIES IN THE DATABASE
    # try:
    #     cnx.is_connected()
    #     print("Connection open")
    #     cursor = cnx.cursor()
    #     delete = ("DELETE FROM timeseries;")
    #     cursor.execute(delete)
    #     cnx.commit()
        
    # except print("Connection is not successfully open"):
    #     pass
    
    try:
        cnx.is_connected()
        print("Connection open")
        cursor = cnx.cursor()
        query = ("SELECT * FROM timeseries;")
        cursor.execute(query)
        results = cursor.fetchall()
    
    except print("Connection is not successfully open"):
        pass
    
    time_count={}
    
    timeseries_df=pd.DataFrame(results,columns=["id","frame_id","name","time","record_source","date"])
    
    timeseries_df.pop('id')
    
    timeseries_raw_data_df = timeseries_df.copy()
    
    timeseries_df=timeseries_df[timeseries_df["frame_id"]==timeseries_df["frame_id"].max()]
    
    
    
    
    for i in timeseries_df["name"].unique():
        timeseries_df[i]=timeseries_df[timeseries_df["name"]==i]["time"]
        timeseries_df[i].fillna(0,inplace=True)
        timeseries_df[i]=timeseries_df[i].cumsum()
        time_count[i]= timeseries_df[i].max()
    
           
    
    ##Split none time % to users
    time_count_no_none=time_count.copy()
    time_count_no_none.pop("none", None)
    time_count_no_none.pop("break_time", None)
    split_percentages={}
    if 'none' in time_count.keys():
        for key in time_count.keys():
            if 'break_time' in time_count.keys():
                percentage = time_count[key]/(sum(time_count.values())-time_count["none"]-time_count["break_time"])
            else:
                percentage = time_count[key]/(sum(time_count.values())-time_count["none"])
            split_percentages[key]=percentage        
        for key,perc in zip(time_count_no_none.keys(),split_percentages):
            time_count[key] += time_count['none'] * split_percentages[key]
        del(time_count['none'])
    
    length_each_frame=timeseries_df["time"].mean()
    
    time_count.pop("break_time",None)
    
    
    
    #STATS
    
    total_video_length=round(timeseries_df["time"].sum(),1)
    upload_date=timeseries_df["date"][-1:].dt.date.to_string()[-10:]
    time_count2=time_count
    time_count2.pop("Unknown",None)
    unique_speakers_identified=len(time_count2.keys())
    video_name=(timeseries_df["record_source"][-1:].to_string()).split("/")[-1]
    
    timeseries_df3=pd.DataFrame.from_dict(time_count2,orient="index")
    if  max(time_count2.values()) > int(120):
          timeseries_df3=timeseries_df3[timeseries_df3.columns]/60
          label= 'minutes'
    else:
        label='seconds'
        
    timeseries_df3.columns=[str("Facetime"+" "+label)]
    
    
    timeseries_df3.sort_values(ascending=False,by=str("Facetime"+" "+label),inplace=True)
    timeseries_df3["Facetime %"]=timeseries_df3[str("Facetime"+" "+label)].apply(lambda x: round(x*100/timeseries_df3.sum(),1))
    timeseries_df3[str("Facetime"+" "+label)]=timeseries_df3[str("Facetime"+" "+label)].round(1)
    
    #SUGESTION FOR FRONTEND:
    # Video:"input.mp4" | Lenght of: 92.8s | Updloaded at: 2020-08-25
    # Totak Speakers identified: 6


    
    print("Video:"+ '"'+str(video_name)+'"'+" | Lenght of:",str(total_video_length)+
          "s | Uploaded at:",str(upload_date))
    print("Totak Speakers identified:",str(unique_speakers_identified))
    
    print(timeseries_df3)
    
    # plot_bars(timeseries_df,length_each_frame,video_name)
    
    return total_video_length, upload_date,unique_speakers_identified,video_name, length_each_frame, timeseries_df3, timeseries_df, timeseries_raw_data_df
