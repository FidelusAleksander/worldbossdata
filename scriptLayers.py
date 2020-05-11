import pandas as pd
import numpy as np
import json
from datetime import timedelta

files=["World Bosses - Azuregos.csv","World Bosses - Kazzak.csv","World Bosses - EDragons.csv"]
col_name="KillTime"
layer_col_name="Layer"

        
def getDataframe(filename,datetime_col_name):
    return pd.read_csv(filename, parse_dates=[datetime_col_name])

def substractTwoHours(df,datetime_col_name):
    df_new=df.copy()
    df_new[datetime_col_name]=df[datetime_col_name]-timedelta(hours=2)
    return df_new

def getRespawnTimersInSeconds(df,datetime_col_name):
    respawnTimers=[]
    for i in range(1,len(df)):
        hours=0
        difference=df[datetime_col_name][i]-df[datetime_col_name][i-1]
        seconds=difference.seconds + difference.days * 24 * 60* 60
        respawnTimers.append(seconds)
    return respawnTimers

        
def getShortestRespawnString(respawnTimersList):
    seconds=min(respawnTimersList)
    minutes=0
    hours=0
    while(seconds>=60):
        seconds-=60
        minutes+=1
    while(minutes>=60):
        minutes-=60
        hours+=1
    return "{}h {}m".format(hours,minutes)

def getLongestRespawnString(respawnTimersList):
    seconds=max(respawnTimersList)
    minutes=0
    hours=0
    while(seconds>=60):
        seconds-=60
        minutes+=1
    while(minutes>=60):
        minutes-=60
        hours+=1
    return "{}h {}m".format(hours,minutes)

def getAverageRespawnString(respawnTimersList):
    seconds=np.mean(respawnTimersList)
    minutes=0
    hours=0
    while(seconds>=60):
        seconds-=60
        minutes+=1
    while(minutes>=60):
        minutes-=60
        hours+=1
    return "{}h {}m".format(hours,minutes)

def getTimestamp(df,datetime_col_name,number):
    size=len(df[datetime_col_name])
    return str(df[datetime_col_name][size-number])

def getEpoch(df,datetime_col_name,number):
    size=len(df[datetime_col_name])
    df_new=substractTwoHours(df,datetime_col_name)
    return df_new[datetime_col_name][size-number].timestamp()

def getLayer(df,layer_col_name,number):
    size=len(df[layer_col_name])
    return str(df[layer_col_name][size-number])

if __name__=="__main__":
	json_list=[]

	for file in files:
	    df=getDataframe(file,col_name)
	    
	    if file=="World Bosses - Azuregos.csv":
	        bossName="Azuregos"
	    elif file=="World Bosses - Kazzak.csv":
	        bossName="Kazzak"
	    elif file=="World Bosses - EDragons.csv":
	        bossName="EDragons"
	    else:
	        raise Exception("Did not recognize data file")

	    wBossObject={
	            "bossName": bossName,
                "lastRespawn" : getTimestamp(df,col_name,1),
                "lastRespawnEpoch":getEpoch(df,col_name,1),
                "lastRespawnLayer":getLayer(df,layer_col_name,1),
                "secondRespawn":getTimestamp(df,col_name,2),
                "secondRespawnEpoch":getEpoch(df,col_name,2),
                "secondRespawnLayer":getLayer(df,layer_col_name,2),
                "thirdRespawn":getTimestamp(df,col_name,3),
                "thirdRespawnEpoch":getEpoch(df,col_name,3),
                "thirdRespawnLayer":getLayer(df,layer_col_name,3),
	            "entries":len(df[col_name])
	            }
	    json_list.append(wBossObject)


	with open("data.json","w") as json_file:
	    json.dump(json_list,json_file)
        

    
    
