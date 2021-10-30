import functools
import re
from io import StringIO
from typing import Union

import numpy as np
import scipy.interpolate as interpolate

import getmap

Integral = Union[int, float]


def get_date(inp: dict) -> str:
    return inp["Observation Time"]


@functools.lru_cache(maxsize=10)
def get_interpolator(data: np.ndarray) -> interpolate.SmoothBivariateSpline:
    return interpolate.SmoothBivariateSpline(data['lat'], data['lon'], data['aurora'])


def get_probability_at(data: np.ndarray, lat: Integral, lon: Integral) -> float:
    interpolator = get_interpolator(data)
    return float(interpolator(lat, lon))


# TODO serive that retrives and names data according to parsed date in a loop
# TODO analyze history
def main(lat: float, lon: float, writeToFile=False, printOulu=True, printMax=True, plot=False):
    content = getmap.get_content()
    aurora_data = getmap.get_data(content)

    if writeToFile:
        date = get_date(content)
        print(date)
        np.savetxt(date, aurora_data)

    if printOulu:
        print("oulu: ", get_probability_at(aurora_data, lat=lat, lon=lon))
    if printMax:
        print("max: ", aurora_data.max())
    if plot:
        import plotMap
        plotMap.plotMap(aurora_data, lat, lon, size=17)


if __name__ == '__main__':
    main(49, 8.6, writeToFile=False, printOulu=True, printMax=True, plot=False)
