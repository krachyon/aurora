import requests


def getmap(fname: str=None) -> str:
    url = "http://services.swpc.noaa.gov/text/aurora-nowcast-map.txt"
    r = requests.get(url)

    if r.status_code == 200:
        if fname:
            with open(fname, "w") as outf:
             outf.write(r.text)
    else:
        raise IOError('fail')

    return r.text