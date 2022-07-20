import fastf1 
import fastf1.plotting 

fastf1.Cache.enable_cache('cache')

session = fastf1.get_session(2022, 'Monaco', 'R')
laps = session.load_laps(with_telemetry=True)




