from collections import namedtuple
from typing import Union, Tuple

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
from aurora import DataContainer

plt.ioff()

latlon = namedtuple("latlon", field_names=("lat", "lon"))
Integral = Union[int, float]


def limitToRange(val: Integral, lim: Tuple[Integral, Integral]) -> Integral:
    return max(min(val, lim[1]), lim[0])


def plot_map(data: DataContainer, lat: Integral, lon: Integral, size: Integral = 10) -> None:
    llc = latlon(limitToRange(lat - size, (-90, 90)), limitToRange(lon - size, (-180, 180)))  # lower left corner
    urc = latlon(limitToRange(lat + size, (-90, 90)), limitToRange(lon + size, (-180, 180)))  # upper right corner
    m = Basemap(projection='stere', lon_0=lon, lat_0=lat,
                llcrnrlon=llc.lon, llcrnrlat=llc.lat, urcrnrlon=urc.lon, urcrnrlat=urc.lat, resolution='i')

    m.drawcoastlines(linewidth=0.4)
    m.drawcountries(linewidth=0.4)

    lon, lat = np.mgrid[0:360:1024j, -90:90:512j]

    mesh = m.pcolormesh(lon, lat, data.interpolator.ev(lon, lat), latlon=True, cmap='viridis', vmin=0, vmax=100)
    m.colorbar(mesh, "right", size="4%", pad='1%')
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(16, 16)

    # plt.savefig('plot.png', dpi=200, pad_inches=0.2, bbox_inches='tight')
    plt.show()


def plot_global(data: DataContainer) -> None:
    lon, lat = np.mgrid[0:360:1000j, -90:90:500j]
    m = Basemap(projection='kav7', lon_0=0, lat_0=0, resolution='l')
    m.drawcoastlines(linewidth=0.4)
    mesh = m.pcolormesh(lon, lat, data.interpolator.ev(lon,lat), latlon=True, cmap='viridis', vmin=0, vmax=100)
    m.colorbar(mesh, "right", size="4%", pad='1%')
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(16, 16)
    plt.show()


def plot_north(data: DataContainer) -> None:
    lon, lat = np.mgrid[0:360:2*1024j, 0:90:2*512j]
    m = Basemap(projection='npaeqd', boundinglat=40, lon_0=0, resolution='l')
    m.drawcoastlines(linewidth=0.4)
    m.drawcountries(linewidth=0.3)
    mesh = m.pcolormesh(lon, lat, data.interpolator.ev(lon, lat), latlon=True, cmap='turbo', vmin=0, vmax=100)
    m.colorbar(mesh, "right", size="4%", pad='1%')
    plt.show()


if __name__ == "__main__":
    import aurora
    import data
    content = data.read_or_request_content()
    dat = aurora.assemble_data(content)
    plot_map(dat, 49, 8.6, size=10)
    #plot_global(dat)
    #plot_north(dat)
