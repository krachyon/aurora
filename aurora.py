import re
from io import StringIO
from typing import Union

import numpy as np
import scipy.interpolate as interpolate

import getmap

Integral = Union[int, float]

def getDate(inp: str) -> str:
    match = re.search(r"^# Product Valid At: (\d\d\d\d-\d\d-\d\d \d\d:\d\d)$", inp, flags=re.MULTILINE)
    if match:
        return match.group(1)
    else:
        raise IOError("file format wrong? did not find date in file")


def getInterpolator(data: np.ndarray) -> interpolate.RectBivariateSpline:
    x = np.linspace(-180, 180, 1024)
    y = np.linspace(-90, 90, 512)
    # Not sure why this function seems to invert x and y, but hey, seems to work like this
    return interpolate.RectBivariateSpline(y, x, data)


def getProbabilityAt(data: np.ndarray, lat: Integral, lon: Integral) -> float:
    interpolator = getInterpolator(data)
    return float(interpolator(lat, lon))


def getData():
    content = getmap.getmap()
    return np.genfromtxt(StringIO(content))

# TODO serive that retrives and names data according to parsed date in a loop
# TODO analyze history
def main(lat: float, lon: float, writeToFile=False, printOulu=True, printMax=True, plot=False):
    content = getmap.getmap()
    if writeToFile:
        date = getDate(content)
        print(date)
        with open(date, 'w') as f:
            f.write(content)

    auroraData = np.genfromtxt(StringIO(content))
    if printOulu:
        print("oulu: ", getProbabilityAt(auroraData, lat=lat, lon=lon))
    if printMax:
        print("max: ", auroraData.max())
    if plot:
        import plotMap
        plotMap.plotMap(auroraData, lat, lon, size=17)


if __name__ == '__main__':
    main(65, 26, writeToFile=False, printOulu=True, printMax=True, plot=False)
