import pandas as pd


def map_drs(drs):
    if drs >= 10:
        return True
    else:
        return False


def remove_pitstops(laps):
    laps_data = laps.copy()
    mask = pd.isnull(laps_data['PitOutTime']) & pd.isnull(laps_data['PitInTime'])
    laps_data = laps_data[mask]
    laps_data = laps_data.drop(['PitOutTime', 'PitInTime'], axis=1)
    return laps_data


def laps_with_incident(laps, incident_times, allclear_times):
    laps_to_remove = []
    # Loop over every incident
    for start_incident, end_incident in zip(incident_times, allclear_times):
        i = 0
        # Find the first impacted lap
        while pd.Timedelta(laps['Time'].iloc[i]) < start_incident:
            i += 1
        laps_to_remove.append(laps['Time'].iloc[i])

        # If the incident is not over by the end of the lap, remove the next lap
        # and repeat until the incident is over
        while pd.Timedelta(laps['Time'].iloc[i]) < end_incident:
            laps_to_remove.append(laps['Time'].iloc[i + 1])
            i += 1
    return laps_to_remove


def remove_incidents(laps, track_status):
    laps_data = laps.copy()
    incident_times = track_status[track_status['Incident'] == True]['Time'].tolist()
    allclear_times = track_status[track_status['Incident'] == False]['Time'].iloc[1:].tolist()
    laps_to_remove = laps_with_incident(laps_data, incident_times, allclear_times)
    laps_data = laps_data[~laps_data["Time"].isin(laps_to_remove)]
    return laps_data