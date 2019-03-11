import getmap
import plotMap
import re
import numpy as np
from io import BytesIO


def getDate(inp: str) -> str:
    match = re.search("^# Product Valid At: (\d\d\d\d-\d\d-\d\d \d\d:\d\d)$", inp, flags=re.MULTILINE)
    if match:
        return match.group(1)
    else:
        raise IOError("file format wrong? did not find date in file")

# TODO serive that retrives and names data according to parsed date in a loop
# TODO analyze history

if __name__ == '__main__':
    content = getmap.getmap()
    date = getDate(content)
    print(date)
    with open(date, 'w') as f:
        f.write(content)

    data = np.genfromtxt(BytesIO(content.encode('utf8')))
    print("oulu: ", plotMap.getProbabilityAt(data, lat=65, lon=26))
    print("max: ", data.max())
    plotMap.plotMap(data, 65, 26, size=17)
