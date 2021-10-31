from collections import namedtuple
from typing import Union, Tuple

import cartopy.crs as ccrs
import cartopy.feature as feature
import matplotlib.pyplot as plt
import numpy as np

from aurora_lib import DataContainer

plt.ioff()

latlon = namedtuple("latlon", field_names=("lat", "lon"))
Integral = Union[int, float]


def limitToRange(val: Integral, lim: Tuple[Integral, Integral]) -> Integral:
    return max(min(val, lim[1]), lim[0])


def plot_map(data: DataContainer, lat: Integral, lon: Integral, size: Integral = 10) -> None:
    xsize, ysize = 1024j, 512j
    lons, lats = np.mgrid[0:360:xsize, -90:90:ysize]
    # oversized grid for mesh
    lonp, latp = np.mgrid[0:360:xsize + 1j, 90:-90:ysize + 1j]
    z = data.interpolator.ev(lons, lats)

    coordsys = ccrs.Stereographic(central_longitude=lon, central_latitude=lat, scale_factor=3)
    ax = plt.axes(projection=coordsys)

    ax.coastlines(resolution='50m')
    ax.add_feature(feature.BORDERS)

    mesh = ax.pcolormesh(lonp, latp, z, transform=ccrs.PlateCarree(), shading='flat',
                         vmin=0, vmax=100, cmap='turbo')

    ax.set_extent([lon - size / 2, lon + size / 2, lat - size / 2, lat + size / 2], ccrs.Geodetic())
    plt.colorbar(mesh)
    plt.show()


def plot_global(data: DataContainer) -> None:
    xsize, ysize = 1024j, 512j
    lon, lat = np.mgrid[0:360:xsize, -90:90:ysize]
    # oversized grid for mesh
    lonp, latp = np.mgrid[0:360:xsize + 1j, 90:-90:ysize + 1j]
    z = data.interpolator.ev(lon, lat)

    fig = plt.figure()

    cordsys = ccrs.Robinson(central_longitude=15)
    ax = fig.add_subplot(1, 1, 1, projection=cordsys)

    mesh = ax.pcolormesh(lonp, latp, z, transform=ccrs.PlateCarree(), shading='flat',
                         vmin=0, vmax=100, cmap='turbo')

    plt.colorbar(mesh)
    ax.coastlines(resolution='50m', linewidth=0.4)

    plt.show()


def plot_north(data: DataContainer) -> None:
    xsize, ysize = 1024j, 512j
    lon, lat = np.mgrid[0:360:xsize, 0:90:ysize]
    # oversized grid for mesh
    lonp, latp = np.mgrid[0:360:xsize + 1j, 0:90:ysize + 1j]
    z = data.interpolator.ev(lon, lat)

    ax = plt.axes(projection=ccrs.Orthographic(central_longitude=15, central_latitude=90))
    ax.coastlines(resolution='50m')
    ax.add_feature(feature.BORDERS)
    mesh = ax.pcolormesh(lonp, latp, z, transform=ccrs.PlateCarree(), shading='flat',
                         cmap='turbo', vmin=0, vmax=100)
    plt.colorbar(mesh)
    plt.show()


if __name__ == "__main__":
    import aurora_lib

    dat = aurora_lib.persistence.latest

    # plot_map(dat, 49, 8.6, size=40)
    plot_global(dat)
    # plot_north(dat)
