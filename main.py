import json
from geopy import distance
from CollatedDataHelper import CollatedDataHelper

from Coordinates import Coordinates
from PriorityQueue import PriorityQueue
from brain import findNearestStop

def getData():
   with open("collated_data.json") as busDatas:
       return busDatas.read()


def dijkstra():
    cd = CollatedDataHelper()
    # Start location : 1.4964559999542668, 103.74374661113058 (Larkin Terminal)
    #End Location : 1.456742090233385, 103.74938268472616 Johor Islamic Complex
    start_loc = Coordinates(1.4964559999542668, 103.74374661113058)
    end_loc = Coordinates(1.456742090233385, 103.74938268472616)

    #print(findStartBus(end_loc))
    start_bus_stop = findNearestStop(start_loc)
    end_bus_stop = findNearestStop(end_loc)
    distanceTo = edgeTo = marked = []
    pq = PriorityQueue()


    pass

def distanceCal(latx, lnbx, laty, lngy):
    pass

def distanceFromXtoB(latx, lngx, latb, lngb):
    pass

def distanceFromBusStop(latCurr, lngCurr, latb, lngb):
    pass

dijkstra()