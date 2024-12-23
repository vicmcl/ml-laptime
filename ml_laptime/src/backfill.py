import fastf1 as ff1
import pickle
from pathlib import Path
import shutil

YEARS = [2019, 2020, 2021]
DRIVER = "VER"
DATA_PATH = Path("../data")
CACHE_PATH = Path("cache")


def set_cache(cache_path=CACHE_PATH):
    if cache_path.exists():
        shutil.rmtree(cache_path)
    cache_path.mkdir(exist_ok=True)
    ff1.Cache.enable_cache(cache_path)


def intersect_schedules(years=YEARS):
    schedules = [
        ff1.get_event_schedule(year)
        .query('EventFormat == "conventional"')["EventName"].values
        for year in years
    ]
    gp_list = set.intersection(*(set(gp_season) for gp_season in schedules))
    gp_list = list(gp_list)
    return gp_list


def main():
    set_cache()
    gp_list = intersect_schedules()

    for year in YEARS:
        sessions = {}
        for gp in gp_list:
            session = ff1.get_session(year, gp, "R")
            session.load()
            driver_laps = session.laps.pick_driver(DRIVER)
            sessions.setdefault(gp, {})["laps"] = driver_laps
            sessions[gp]["weather"] = session.weather_data
            sessions[gp]["telemetry"] = driver_laps.telemetry
            sessions[gp]["status"] = session.track_status

        with open(DATA_PATH / f"races_{year}.pkl", "wb") as f:
            pickle.dump(sessions, f)

    shutil.rmtree(CACHE_PATH)


if __name__ == "__main__":
    main()
