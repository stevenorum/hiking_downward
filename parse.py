#!/usr/bin/env python

import json
from math import radians, cos, sin, asin, sqrt

def haversine(start, end):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    from http://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
    """
    # convert decimal degrees to radians 
    lat1, lon1, lat2, lon2 = map(radians, [start[0], start[1], end[0], end[1]])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 3956 # Radius of earth in miles. Use 6371 for kilometers
    return c * r

# No, these aren't the exact locations.
HOME = (37.550844, -77.456137)
WORK = (38.969759, -77.383893)

class Hike(object):
    def __init__(self, line):
        parts = line.split(", ")
        parts = [", ".join(parts[:-10])] + parts[-10:]
        parts = [json.loads(p) for p in parts]
        self.title = parts[0]
        self.location = (parts[1], parts[2])
        self.url = parts[3]
        self.length = parts[4]
        self.difficulty = parts[5]
        self.streams = parts[6]
        self.views = parts[7]
        self.gain = parts[8]
        self.solitude = parts[9]
        self.camping = parts[10]
        self.home = self.homedist()
        self.work = self.workdist()

    def homedist(self):
        return haversine(HOME, self.location)

    def workdist(self):
        return haversine(WORK, self.location)

    def __str__(self):
        format_string = "{title}: {length} miles, {gain} elevation gain, {difficulty} difficulty, {home} miles from home, {work} miles from work"
        return format_string.format(**self.__dict__)

hikes = []
with open("hikes.csv","r") as f:
    hikes = [Hike(l.strip()) for l in f.readlines() if l.strip()]

close_to_home = lambda x: x.home
close_to_work = lambda x: x.work
hikes.sort(key=close_to_work, reverse=True)
for hike in hikes:
    print(str(hike))
    print(hike.location)
