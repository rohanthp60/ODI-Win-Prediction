from pathlib import Path
import json

def load_data():
    folder = Path("../data/raw")
    data = []

    for path in folder.glob("*.json"):
        with path.open("r", encoding="utf-8") as f:
            data.append(json.load(f))

    return data

def filter_with_nation_winners(data):
    data = [d for d in data 
            if "winner" in d["info"]["outcome"] and 
            d["info"]["outcome"]["winner"][-2:] != "XI" and
            "method" not in d["info"]["outcome"] and
            d["info"]["gender"] == "male"]
    innings_keys = lambda x: set(list(data[x]['innings'][0].keys()) + list(data[x]['innings'][1].keys()))
    data = [d for i, d in enumerate(data) 
            if not (set(["penalty_runs", "miscounted_overs", "absent_hurt"]) & innings_keys(i))
            and "target" in d['innings'][1]
            ]
    data = [d for d in data
            if d['innings'][1]['target']['overs'] == 50]
    return data
