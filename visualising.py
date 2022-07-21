from main import df
from api_F1_data import laps, session
import seaborn as sns 
import matplotlib.pyplot as plt
import fastf1
import pandas as pd

# -------- Preprocessing of selected data ----------------- #

drivers = ['VER','PER','LEC','SAI','VET','STR']
first_half = laps[(laps['LapNumber'] < 18)]
mask = first_half.Driver.isin(drivers)
driver_laps = first_half[mask]
driver_laps.LapTime.values.astype('timedelta64[ms]')
driver_laps = driver_laps.replace(driver_laps.LapTime.values, driver_laps.LapTime.values/1000000000)

timings = fastf1.api.timing_data(session.api_path)

new = pd.DataFrame(timings[1].Driver, columns=['Driver'])
new['GapToLeader'] = timings[1].GapToLeader
new['Time'] = timings[1].Time
new['Position'] = timings[1].Position
new['IntervalToPositionAhead'] = timings[1].IntervalToPositionAhead

sample = pd.DataFrame()
sample['LEC'] = timings[0].LapTime[timings[0].Driver == '16'].values
sample['VER'] = timings[0].LapTime[timings[0].Driver == '1'].values
sample['SAI'] = timings[0].LapTime[timings[0].Driver == '55'].values
sample['PER'] = timings[0].LapTime[timings[0].Driver == '11'].values

# ------- trying to create the time gap between sainz and perez but it didnt quite work ----- #
diff_SAI_PER = list()
previous_v = 0
for i in range(64):
     if i == 0:
        print('nothing')
     else:
        v = sample['PER'][i].total_seconds() - sample['SAI'][i].total_seconds()
        delta_time = v + previous_v
        diff_SAI_PER.append(delta_time)
        previous_v = delta_time

# ----- selecting certain laps for Perez to compare the difference in wet and intermediate tyres lap time ----- #

lap15 = laps[(laps['LapNumber'] == 15)]
lap18 = laps[(laps['LapNumber'] == 18)]
lap15_PER = lap15.pick_driver('PER').get_car_data().add_distance()
lap18_PER = lap18.pick_driver('PER').get_car_data().add_distance()

# ------------- Using Matplotlib -------------- #
plt.plot(lap15_PER['Distance'],lap15_PER['Speed'], label='Lap 15')
plt.plot(lap18_PER['Distance'],lap18_PER['Speed'], label='Lap 18')
plt.title('2022 Formula 1 Grand Prix De Monaco 2022 Race')
plt.xlabel('Distance [m]', fontsize=14)
plt.ylabel('Speed',fontsize=14)
plt.legend()
plt.show()

# -------- Using Seaborn ----------- #

sns.lineplot(data=new, x='Time', y='Position', hue='Driver').set(title="")
sns.lineplot(data=driver_laps, x='LapNumber', y='LapTime', hue='Driver').set(title="")
sns.set(font_scale=1)
plt.ylim(reversed(plt.ylim()))
plt.title('2022 Formula 1 Grand Prix de Monaco 2022 Race')
