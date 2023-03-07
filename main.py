import json
from geopy import distance

from Coordinates import Coordinates
from brain import findNearestStop

def dijkstra():
    # Start location : 1.4964559999542668, 103.74374661113058 (Larkin Terminal)
    #End Location : 1.456742090233385, 103.74938268472616 Johor Islamic Complex
    start_loc = Coordinates(1.4964559999542668, 103.74374661113058)
    end_loc = Coordinates(1.456742090233385, 103.74938268472616)

    location3 = Coordinates(1.4860478,103.7544695)
    #print(findStartBus(start_loc))
    #print(findStartBus(end_loc))
    print(findNearestStop(location3))







    pass

def distanceCal(latx, lnbx, laty, lngy):
    pass

def distanceFromXtoB(latx, lngx, latb, lngb):
    pass

def distanceFromBusStop(latCurr, lngCurr, latb, lngb):
    pass

dijkstra()