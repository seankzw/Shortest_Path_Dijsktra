import heapq
import json
import sys
from geopy import distance
from CollatedDataHelper import CollatedDataHelper

from Coordinates import Coordinates
from brain import findNearestStop

def getCollatedData():
    f = open("collated_data.json")
    data = json.loads(f.read())
    return data

def getOverviewData():
    f = open("excel_overview.json")
    data = json.loads(f.read())
    return data

def dijkstra(start_node):
    data = getCollatedData()
    unvisited_nodes = list(data.keys())
    shortest_path = {}
    previous_nodes = {}

    #Initialise all the bus stops to infinity and start node to 0
    for node in unvisited_nodes:
        shortest_path[node] = sys.maxsize
    shortest_path[start_node] = 0

    while unvisited_nodes:
        #get the minimum distance of the current stop
        curr_shortest_route = None
        for eachStop in unvisited_nodes:

            if curr_shortest_route == None:
                curr_shortest_route= eachStop
            elif shortest_path[eachStop] < shortest_path[curr_shortest_route]:
                curr_shortest_route = eachStop
        # get destinations :
        edges = data[curr_shortest_route]["edgeTo"]
        for eachDestination in edges:
            tent_val = shortest_path[curr_shortest_route] + data[curr_shortest_route]["edgeTo"][eachDestination]
            #print("Unvisited node = {}".format(unvisited_nodes))
            if tent_val < shortest_path[eachDestination]:
                shortest_path[eachDestination] = tent_val
                previous_nodes[eachDestination] = curr_shortest_route


        unvisited_nodes.remove(curr_shortest_route)


    #print("Previous node = {}".format(previous_nodes))
    #print("shortest path = {}".format(shortest_path))




    return previous_nodes, shortest_path


def getShortestPath(previous_nodes, shortest_path, start, end):
    #print(shortest_path[end])
    path = []
    destination = end
    data = getOverviewData()

    while destination != start:
        path.append({
            "bus_stop_name": destination,
            "coordinates" : (data[destination]["lat"], data[destination]["lng"]),
            "bus": data[destination]["operating_buses"]
        })

        destination = previous_nodes[destination]

    path.append({
        "bus_stop_name": start,
        "coordinates" : (data[start]["lat"], data[start]["lng"]),
        "bus": data[start]["operating_buses"],
    })

    return path





# Start location : 1.4964559999542668, 103.74374661113058 (Larkin Terminal)
#End Location : 1.456742090233385, 103.74938268472616 Johor Islamic Complex
#start_loc = Coordinates(1.4964559999542668, 103.74374661113058)
#end_loc = Coordinates(1.456742090233385, 103.74938268472616)

#Start location : CIMB BANK : 1.4888638795941063, 103.71242062086549
#END LOCATION : bef Econsave @ Senai" : 1.6102010601670786, 103.65715287633772
#start_loc = Coordinates(1.5423777121603113, 103.62969894227055) #AEON
#end_loc = Coordinates(1.6349379250179437, 103.66630691168017) # Senai Airport Terminal

#start_node = findNearestStop(start_loc)
#end_bus_stop = findNearestStop(end_loc)

#previous_node, shortest_path = dijkstra(start_node)
#path = getShortestPath(previous_node, shortest_path, start_node, end_bus_stop)
#print(path)