#file  -- helpers.py --

import var
from datetime import datetime, timedelta

# Retrieve N bytes of data in big endian from passed data set starting at passed offset
def readBE(data, offset, n):
    return (int.from_bytes(data[offset:offset+(n)], byteorder='big'))

# Retrieve N bytes of data in little endian from passed data set starting at passed offset
def readLE(data, offset, n):
    return (int.from_bytes(data[offset:offset+(n)], byteorder='little'))

# Read and return number of trophies
def getTrophyCount():
    with open(var.TITLE, 'r+b') as f:
        trptitle = f.read()
    return readBE(trptitle, var.NUMOFTROPHY, 1)

# Convert a time stamp of format YYYYMMDDHHMMSS to Sony bytes
def encodeTimestamp(dt):
    try:
        dt = datetime.strptime(dt, '%Y%m%d%H%M%S')
        dt += datetime.utcnow() - dt
        timestamp = (dt - datetime(1, 1, 1)) / timedelta(microseconds=1)
        return bytes.fromhex('{:016X}'.format(int(timestamp)))
    except:
        print('Invalid timestamp format')
        exit()