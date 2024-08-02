import pandas as pd
from utils import remove_pitstops, remove_incidents, map_drs

COMPOUND_MAP = {'SOFT': 1.0, 'MEDIUM': 2.0, 'HARD': 3.0}
COLUMNS_TELEMETRY = ['SessionTime', 'Throttle', 'Brake', 'DRS']
COLUMNS_WEATHER = ['Time', 'TrackTemp', 'WindSpeed']
COLUMNS_LAPS = [
    'Time', 'LapNumber', 'Stint', 'SpeedI1', 'SpeedI2', 'SpeedFL', 'SpeedST',
    'Compound', 'TyreLife', 'LapTime', 'PitOutTime', 'PitInTime'
]


def process_track_status(data, gp, year):
    track_status = data[year][gp]['status'].copy()
    track_status['Incident'] = track_status['Status'].map(lambda s: False if s == '1' else True)
    mask = track_status['Incident'] & track_status['Incident'].shift(1)
    track_status = track_status[~mask][['Time', 'Incident']]
    return track_status


def process_lap_data(data, gp, year):
    laps_data = data[year][gp]['laps'][COLUMNS_LAPS].copy()
    laps_data['Season'] = year
    laps_data = laps_data.reset_index().drop('index', axis=1)
    laps_data['Compound'] = laps_data['Compound'].map(lambda x: COMPOUND_MAP.get(x, 0.0))
    laps_data = remove_pitstops(laps_data)
    track_status = process_track_status(gp, year)
    laps_data = remove_incidents(laps_data, track_status)
    return laps_data


def process_telemetry_data(data, gp, year, laps):
    telemetry_data = data[year][gp]['telemetry'][COLUMNS_TELEMETRY].copy()
    telemetry_with_laps = pd.merge_asof(
        telemetry_data,
        laps[['Time', 'LapNumber']],
        left_on='SessionTime',
        right_on='Time',
        direction='forward'
    ).drop('Time', axis=1)
    telemetry_with_laps.loc[:, 'DRS'] = telemetry_with_laps['DRS'].map(map_drs)
    telemetry_avg = telemetry_with_laps.groupby('LapNumber').mean()
    return telemetry_avg


def process_weather_data(data, gp, year):
    weather_data = data[year][gp]['weather'][COLUMNS_WEATHER].copy()
    return weather_data


def merge_data(laps, weather, telemetry):
    # Merge laps and weather
    merged_data = pd.merge_asof(
        laps, weather, on='Time', direction='nearest'
    ).set_index('LapNumber').drop('Time', axis=1)
    # Merge telemetry
    merged_data = pd.concat([merged_data, telemetry], axis=1).reset_index()
    merged_data = merged_data.drop('SessionTime', axis=1)
    # Laptime to seconds
    merged_data.loc[:, 'LapTime'] = merged_data['LapTime'].map(
        lambda x: x.total_seconds()
    )
    return merged_data


def preprocess_data(data, gp, year):
    laps = process_lap_data(data, gp, year)
    weather = process_weather_data(data, gp, year)
    telemetry = process_telemetry_data(data, gp, year, laps)
    merged_data = merge_data(laps, weather, telemetry)
    return merged_data
