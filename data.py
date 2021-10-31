import requests

import json
from pathlib import Path
import datetime

OBSTIME = 'Observation Time'
PREDTIME  = 'Forecast Time'
COORDS = 'coordinates'

persistence_folder = Path = Path('persistence')
latest = persistence_folder/'ovation_aurora_latest.json'


def get_latest_content() -> dict[str, any]:
    print('getting latest data')
    url = "https://services.swpc.noaa.gov/json/ovation_aurora_latest.json"
    r = requests.get(url)

    if r.status_code != 200:
        raise IOError('fail')

    parsed = (json.loads(r.text))
    return parsed


def get_datetime(timestring: str):
    return datetime.datetime.strptime(timestring, '%Y-%m-%dT%H:%M:%SZ')


def read_or_request_content(persistence_folder: Path = persistence_folder):
    if latest.exists():
        with open(latest, 'r') as f:
            content = json.load(f)
        diff = datetime.datetime.utcnow()-get_datetime(content[OBSTIME])
        if diff < datetime.timedelta(minutes=10):
            return content

    content = get_latest_content()
    with open(latest, 'w') as f:
        json.dump(content, f)

    return content


if __name__=='__main__':
    content = read_or_request_content()

