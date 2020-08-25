

import mysql.connector
import pandas as pd
from Plot_graphs import plot_bars

cnx = mysql.connector.connect(user = 'root', password = 'tasmania',host ='localhost',
                              database = 'project9')

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

timeseries_df=pd.DataFrame(results,columns=["name","time","record_source","date"])

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

print(time_count,"seconds")
plot_bars(timeseries_df,length_each_frame)

