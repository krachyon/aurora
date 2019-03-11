from collections import namedtuple
from typing import Union, Tuple

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap

plt.ioff()

latlon = namedtuple("latlon", field_names=("lat", "lon"))
Integral = Union[int, float]


def limitToRange(val: Integral, lim: Tuple[Integral, Integral]) -> Integral:
    return max(min(val, lim[1]), lim[0])


def plotMap(data: np.ndarray, lat: Integral, lon: Integral, size: Integral = 10) -> None:
    llc = latlon(limitToRange(lat - size, (-90, 90)), limitToRange(lon - size, (-180, 180)))  # lower left corner
    urc = latlon(limitToRange(lat + size, (-90, 90)), limitToRange(lon + size, (-180, 180)))  # upper right corner
    m = Basemap(projection='stere', lon_0=lon, lat_0=lat,
                llcrnrlon=llc.lon, llcrnrlat=llc.lat, urcrnrlon=urc.lon, urcrnrlat=urc.lat, resolution='i')

    m.drawcoastlines(linewidth=0.4)
    m.drawcountries(linewidth=0.4)

    lon, lat = np.meshgrid(np.linspace(-180, 180, 1024), np.linspace(-90, 90, 512))
    mesh = m.pcolormesh(lon, lat, data, latlon=True, cmap=plt.cm.jet, vmin=0, vmax=100)
    m.colorbar(mesh, "right", size="4%", pad='1%')
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(16, 16)

    # plt.savefig('plot.png', dpi=200, pad_inches=0.2, bbox_inches='tight')
    plt.show()


def plotGlobal(data: np.ndarray) -> None:
    lon, lat = np.meshgrid(np.linspace(-180, 180, 1024), np.linspace(-90, 90, 512))
    m = Basemap(projection='kav7', lon_0=0, lat_0=0, resolution='l')
    m.drawcoastlines(linewidth=0.4)
    mesh = m.pcolormesh(lon, lat, data, latlon=True, cmap=plt.cm.jet, vmin=0, vmax=100)
    m.colorbar(mesh, "right", size="4%", pad='1%')
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(16, 16)
    plt.show()


if __name__ == "__main__":
    dat = np.genfromtxt('nowcast.txt')
    plotMap(dat, 65, 26, size=10)
