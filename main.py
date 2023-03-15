import heapq
import json
import sys
from geopy import distance
from CollatedDataHelper import CollatedDataHelper

from Coordinates import Coordinates
from brain import findNearestStop

def getData():
    f = open("collated_data.json")
    data = json.loads(f.read())
    return data

def dijkstra(start_node):
    data = getData()
    # Start location : 1.4964559999542668, 103.74374661113058 (Larkin Terminal)
    #End Location : 1.456742090233385, 103.74938268472616 Johor Islamic Complex
    start_loc = Coordinates(1.4964559999542668, 103.74374661113058)
    end_loc = Coordinates(1.456742090233385, 103.74938268472616)
    start_node = findNearestStop(start_loc)
    end_bus_stop = findNearestStop(end_loc)
    unvisited_nodes = list(data.keys())
    shortest_path = previous_nodes = {}

    #Initialise all the bus stops to infinity and start node to 0
    for node in unvisited_nodes:
        shortest_path[node] = sys.maxsize
    shortest_path[start_node] = 0

    while unvisited_nodes:
        #get the minimum distance of the current stop
        curr_shortest_route = None
        for eachStop in unvisited_nodes:
            print("shortest_path[eachStop] = {}".format(shortest_path[eachStop]))
            print()

            if curr_shortest_route == None:
                curr_shortest_route= eachStop
            elif shortest_path[eachStop] < shortest_path[curr_shortest_route]:
                curr_shortest_route = eachStop
        # get destinations :
        edges = data[curr_shortest_route]["edgeTo"]
        for eachDestination in edges:
            tent_val = shortest_path[curr_shortest_route] + data[curr_shortest_route]["edgeTo"][eachDestination]
            #print("Unvisited node = {}".format(unvisited_nodes))
            print("tent val = {}".format(tent_val))
            print("eachDestination = {}".format(eachDestination))
            if tent_val < shortest_path[eachDestination]:
                shortest_path[eachDestination] = tent_val
                previous_nodes[eachDestination] = curr_shortest_route

        unvisited_nodes.remove(curr_shortest_route)

    return previous_nodes, shortest_path



'''
    shortest_path = {
        "Larkin Terminal": 0
        "Perjabat": inf
        "Something": inf
        "That_thing":inf
    }

    current_min_node = Larkin Terminal

    -- Get destination that larkin terminal go

    Loop through each destination
    - tentative_val = shortest_path["Larkin Terminal"] + distance to the destination
    - if tentative_val is shorter than in shortest_path
        -   replace the shortest path and update destination
    remove the node from unvisited
'''




def distanceCal(latx, lnbx, laty, lngy):
    pass

def distanceFromXtoB(latx, lngx, latb, lngb):
    pass

def distanceFromBusStop(latCurr, lngCurr, latb, lngb):
    pass

test = dijkstra(1)
print(test)