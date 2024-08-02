import fastf1 as ff1
import pickle
from pathlib import Path
import shutil

years = [2019, 2020, 2021]
driver = "VER"

cache = Path("cache")
cache.mkdir(exist_ok=True)
ff1.Cache.enable_cache(cache)

gp_list = set.intersection(
    *(set(
        ff1.get_event_schedule(year)
        .query('EventFormat == "conventional"')["EventName"]
        .values
    ) for year in years)
)
gp_list = list(gp_list)
print(gp_list)

for year in years:
    sessions = {}
    for gp in gp_list:
        session = ff1.get_session(year, gp, "R")
        session.load()
        ver_laps = session.laps.pick_driver(driver)
        sessions.setdefault(gp, {})["laps"] = ver_laps
        sessions[gp]["weather"] = session.weather_data
        sessions[gp]["telemetry"] = ver_laps.telemetry
        sessions[gp]["status"] = session.track_status

    with open(f"races_{year}.pkl", "wb") as f:
        pickle.dump(sessions, f)

shutil.rmtree(cache)
