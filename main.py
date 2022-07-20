import seaborn as sns
import pandas as pd
import numpy as np
import re

df = pd.read_csv(r"/Users/ciward/MyFolder/MyFolder/TrackDataExample.csv")
distance = df.LapDistance.values
speed = df.CarVelocity.values 
time = list()
stop = len(distance)-1

for count, i in enumerate(distance[0:stop]):

    if count == 0:
        time.append(0)

    if count == len(distance):
        time.append(1000)
    
    if count > 0 & (count != len(distance)):
        dist = distance[count+1] - distance[count]
        vel = np.mean(speed[count+1] + speed[count])
        seconds = dist/vel + time[count-1]
        time.append(seconds)

time.append(169)
df.insert(2,"Time",time)
acceleration = np.gradient(df.CarVelocity)
df.insert(4,"Acceleration",acceleration)
rake = df.RearRideHeight - df.FrontRideHeight
df.insert(11,"Rake",rake)

# --------------------------------- Implementing Reusable Code ---------------------------- #
def CornerSpeed(part):
    return{
        'T1': 'Low Speed',
        'T2': 'Medium Speed',
        'T3': 'Non-Limited',
        'T4': 'Medium Speed',
        'T5': 'Non-Limited',
        'T6': 'High Speed',
        'T7': 'High Speed',
        'T8': 'Low Speed',
        'T9 & T10': 'Low Speed',
        'T11': 'Medium Speed',
        'T12': 'High Speed',
        'T13': 'Medium Speed',
        'T14 & T15': 'Medium Speed'

    }[part]

# -------------------------- Cleaning the Categories ----------------------------------------------- #
r = re.compile("T[0-9]+$")

for i in range(len(df)):

    if len(df.Straight[i] + df.Corner[i]) < 3:

        if df.Time[i] == 0:

            df.Straight[i] == "Start - T1"
        
        else:
            acc_mean = np.mean(df.Acceleration[i-1] + df.Acceleration[i] + df.Acceleration[i+1])

            if acc_mean < df.Acceleration[i-1]:

                if len(df.Straight[i-1]) > 3:
                    part = r.search(df.Straight[i-1]).group()

                    if part == "T14":
                        part = "T14 & T15"
                    
                    df.Corner[i] = part
                    df.CornerSpeed[i] = CornerSpeed(part)
                    df.CornerPhase[i] = "Braking"
                
                else:

                    df.Corner[i] = df.Corner[i-1]
                    df.CornerSpeed[i] = df.CornerSpeed[i-1]
                    df.CornerPhase[i] = df.CornerPhase[i-1]

            else:
               if(acc_mean > df.Acceleration[i-1]) and len(df.Straight[i-1])>3:
                   df.Straight[i] = df.Straight[i-1]
               
               else:

                 if df.Corner[i-1] == "T14":
                    df.Corner[i] = "T14 & T15"

                    df.Corner[i] = df.Corner[i-1]
                    df.CornerSpeed[i] = df.CornerSpeed[i-1]
                    df.CornerPhase[i] = df.CornerPhase[i-1]

# --------------------------------- Minor Changes to the DF Structure ----------------------------------------- #

df.rename(columns={"LapDistance":"Distance", "CarVelocity":"Velocity"}, inplace=True)

df = df.round({'Distance':2,'Velocity':3,'Time':3,'Acceleration':5,'FrontRideHeight':2,'RearRideHeight':2,
            'Rake':3,'TimeToCarAhead':4,'TyreTempFR':2,'TyreTempRL':2,'TyreTempRR':2})

df.TimeToCarAhead = df.TimeToCarAhead.interpolate(method='linear')



