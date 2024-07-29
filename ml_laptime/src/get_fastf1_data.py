import fastf1 as ff1
import pickle
from pathlib import Path
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("year", type=int)
year = parser.parse_args().year

cache = Path("cache")
cache.mkdir(exist_ok=True)
ff1.Cache.enable_cache(cache)

schedule = (
    ff1.get_event_schedule(year)
    .query('EventFormat == "conventional"')["EventName"]
    .values
)

sessions = {}
for i, gp in enumerate(schedule):
    session = ff1.get_session(year, i + 1, "R")
    session.load()
    ver_laps = session.laps.pick_driver("VER")
    sessions.setdefault(gp, {})["laps"] = ver_laps
    sessions[gp]["weather"] = session.weather_data
    sessions[gp]["telemetry"] = ver_laps.telemetry

with open(f"races_{year}.pkl", "wb") as f:
    pickle.dump(sessions, f)

cache.rmdir()
