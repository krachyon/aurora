import dataclasses
import datetime
import functools
import re
from io import StringIO
from typing import Union, Optional

import scipy.interpolate as interpolate
import numpy as np
from numpy.lib.recfunctions import unstructured_to_structured

from data import read_or_request_content, get_datetime, COORDS, OBSTIME, PREDTIME

Integral = Union[int, float]

@dataclasses.dataclass
class DataContainer:
    structured: np.ndarray

    lats: np.ndarray
    lons: np.ndarray
    llats: np.ndarray
    llons: np.ndarray
    z: np.ndarray

    obstime: datetime.datetime
    predtime: datetime.datetime

    _interpolator: Optional[interpolate.RectBivariateSpline] = dataclasses.field(default=None, init=False, repr=False)

    @property
    def interpolator(self):
        if self._interpolator is None:
            self._interpolator = interpolate.RectBivariateSpline(self.lons, self.lats, self.z)
        return self._interpolator


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


def get_probability_at(data: DataContainer, lat: Integral, lon: Integral) -> float:
    return float(data.interpolator(lat, lon))


# TODO serive that retrives and names data according to parsed date in a loop
# TODO analyze history
def main(lat: float, lon: float, printLocation=True, printMax=True, plot=False):
    content = read_or_request_content()
    aurora_data = assemble_data(content)

    if printLocation:
        print(f'Location {lat=}, {lon=}: ', get_probability_at(aurora_data, lat=lat, lon=lon))
    if printMax:
        print('max: ', aurora_data.structured['aurora'].max())
    if plot:
        import plotMap
        plotMap.plot_map(aurora_data, lat, lon, size=17)


if __name__ == '__main__':
    main(49, 8.6, printLocation=True, printMax=True, plot=True)
