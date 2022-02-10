from utilities import check_callsign

import pandas as pd
import numpy as np
import json


def convert_fr24(js):
    
    data = {
        "time": [],
        "callsign": [],
        "latitude": [],
        "longitude": [],
        "altitude": [],
        "ground_speed": [],
        "heading_angle": []
    }

    for k in js:
        if isinstance(js[k], list):
            
            # Check if the list has the correct length
            # Should have length 18
            if len(js[k]) < 18:
                print("Error: Wrong entry length")
                print(js[k])
                print()
                continue

            row = js[k]
            data["time"].append(pd.Timestamp(row[10], unit="s"))
            data["callsign"].append(check_callsign(row[16]))
            data["latitude"].append(row[1])
            data["longitude"].append(row[2])
            data["altitude"].append(row[4])
            data["ground_speed"].append(row[5])
            data["heading_angle"].append(row[3])

    data["source"] = ["flightradar24" for _ in range(len(data["time"]))]
    df = pd.DataFrame.from_dict(data)
    df = df.set_index("time")


    # Pandas NaN gives a lot of problems
    # Ad-hoc solution: Add an extra first column containing np.nan,
    # which somehow makes np.nan writeable afterward
    df = df.assign(a=pd.Series([np.nan for _ in range(len(df))]).values)

    return df
