import requests
import numpy as np
from numpy.lib.recfunctions import unstructured_to_structured
import json


def get_content(fname: str = None) -> np.ndarray:
    url = "https://services.swpc.noaa.gov/json/ovation_aurora_latest.json"
    r = requests.get(url)

    if r.status_code == 200:
        if fname:
            with open(fname, "w") as outf:
                outf.write(r.text)
    else:
        raise IOError('fail')

    parsed = (json.loads(r.text))
    return parsed


def get_data(content):
    dtype = np.dtype([('lon', int), ('lat', int), ('aurora', int)])
    array = unstructured_to_structured(np.array(content['coordinates']), dtype=dtype)
    return array