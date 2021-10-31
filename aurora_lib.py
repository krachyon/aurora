import dataclasses
import datetime
import json
import logging
from pathlib import Path
from typing import Union, Optional

import numpy as np
import requests
import scipy.interpolate as interpolate
from numpy.lib.recfunctions import unstructured_to_structured

Integral = Union[int, float]

OBSTIME = 'Observation Time'
PREDTIME = 'Forecast Time'
COORDS = 'coordinates'


def get_latest_content() -> dict[str, any]:
    logging.info('getting latest data')
    url = "https://services.swpc.noaa.gov/json/ovation_aurora_latest.json"
    r = requests.get(url)

    if r.status_code != 200:
        raise IOError('fail')

    parsed = (json.loads(r.text))
    return parsed


def get_datetime(timestring: str):
    return datetime.datetime.strptime(timestring, '%Y-%m-%dT%H:%M:%SZ')


@dataclasses.dataclass
class DataContainer:
    structured: np.ndarray

    # unique lat, lon
    lats: np.ndarray
    lons: np.ndarray
    # grid data, same shape
    llats: np.ndarray
    llons: np.ndarray
    z: np.ndarray

    # metadata
    obstime: datetime.datetime
    predtime: datetime.datetime

    _interpolator: Optional[interpolate.RectBivariateSpline] = dataclasses.field(default=None, init=False, repr=False)

    @property
    def interpolator(self):
        """returns object that can be called with either __call__(lon, lat) or .ev([lon,...], [lat,...])"""
        if self._interpolator is None:
            self._interpolator = interpolate.RectBivariateSpline(self.lons, self.lats, self.z)
        return self._interpolator


class DataPersistence:

    def __init__(self, persistence_folder):
        self._persistence_folder = persistence_folder
        self._history: dict[datetime, DataContainer] = dict()

        for input_file in persistence_folder.glob('*.json'):
            with open(input_file, 'r') as f:
                content = json.load(f)
                data = assemble_data(content)
                self._history[data.obstime] = data

    def get_latest_data(self) -> DataContainer:
        content = get_latest_content()
        filename = self._persistence_folder / (content[OBSTIME] + '.json')
        with open(filename, 'w') as f:
            json.dump(content, f)
        data = assemble_data(content)
        self._history[data.obstime] = data
        return data

    @property
    def latest(self) -> DataContainer:
        latest = self._history[sorted(self._history)[0]]
        diff = datetime.datetime.utcnow() - latest.obstime

        if diff < datetime.timedelta(minutes=10):
            return latest
        else:
            return self.get_latest_data()

    @property
    def histoy(self) -> dict[datetime, DataContainer]:
        return self._history


def assemble_data(content: dict[str, any]) -> DataContainer:
    dtype = np.dtype([('lon', int), ('lat', int), ('aurora', int)])
    structured_array = unstructured_to_structured(np.array(content[COORDS]), dtype=dtype)

    structured_array.sort(order=['lon', 'lat'])
    lons = np.unique(structured_array['lon'])
    lats = np.unique(structured_array['lat'])
    shape = (len(lons), len(lats))
    llons = structured_array['lon'].reshape(shape)
    llats = structured_array['lat'].reshape(shape)
    z = structured_array['aurora'].reshape(shape)

    ret = DataContainer(structured=structured_array,
                        lats=lats,
                        lons=lons,
                        llons=llons,
                        llats=llats,
                        z=z,
                        obstime=get_datetime(content[OBSTIME]),
                        predtime=get_datetime(content[PREDTIME])
                        )
    return ret


def get_probability_at(lat: Integral, lon: Integral) -> float:
    data = persistence.latest
    return float(data.interpolator(lat, lon))


def main(lat: float, lon: float, print_location=True, print_max=True, plot=False):
    aurora_data = persistence.latest

    if print_location:
        print(f'Location {lat=}, {lon=}: ', get_probability_at(lat=lat, lon=lon))
    if print_max:
        print('max: ', aurora_data.structured['aurora'].max())
    if plot:
        import plot_map
        plot_map.plot_map(aurora_data, lat, lon, size=40)


persistence_folder: Path = Path('./persistence')
persistence = DataPersistence(persistence_folder)

if __name__ == '__main__':
    main(49, 8.6, print_location=True, print_max=True, plot=True)
