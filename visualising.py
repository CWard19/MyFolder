from main import df
from api_F1_data import laps, session
import seaborn as sns 
import matplotlib.pyplot as plt

# -------- Preprocessing of selected data ----------------- #

drivers = ['VER','PER','LEC','SAI','VET','STR']
first_half = laps[(laps['LapNumber'] < 18)]
mask = first_half.Driver.isin(drivers)
driver_laps = first_half[mask]
driver_laps = driver_laps.replace(driver_laps.LapTime.values, driver_laps.LapTime.values/1000000000)

sns.lineplot(data=driver_laps, x='LapNumber', y='LapTime', hue='Driver').set(title="")
sns.set(font_scale=1)
plt.ylim(reversed(plt.ylim()))
plt.title('2022 Formula 1 Grand Prix de Monaco 2022 Race')
print('hello')