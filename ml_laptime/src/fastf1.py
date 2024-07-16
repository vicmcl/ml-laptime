import fastf1 as ff1
import pickle

ff1.Cache.enable_cache('.')
schedule = ff1.get_event_schedule(2021).query(
    'EventFormat == "conventional"'
)['EventName'].values

sessions = {}
for i, gp in enumerate(schedule):
    session = ff1.get_session(2021, i + 1, 'R')
    session.load()
    ver_laps = session.laps.pick_driver('VER')
    sessions.setdefault(gp, {})['laps'] = ver_laps
    sessions[gp]['weather'] = session.weather_data
    sessions[gp]['telemetry'] = ver_laps.telemetry

with open('races_2021.pkl', 'wb') as f:
    pickle.dump(sessions, f)