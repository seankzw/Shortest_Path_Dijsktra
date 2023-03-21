import heapq
import json
import sys
from geopy import distance
from CollatedDataHelper import CollatedDataHelper

from Coordinates import Coordinates
from brain import findNearest5Stop, findNearestStop

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


def getShortestPathFromList(previous_nodes, start, end_stops):
    data = getOverviewData()
    collated_data = getCollatedData()
    shortest_length = float('inf')
    shortest_path = []

    for i in range(len(end_stops)):
        destination = end_stops[i]
        curr_length = 0
        path = []
        while destination != start:
            path.append({
                "bus_stop_name": destination,
                "coordinates" : (data[destination]["lat"], data[destination]["lng"]),
                "bus": data[destination]["operating_buses"]
            })

            prev_dest = previous_nodes[destination]
            curr_length+= collated_data[prev_dest]["edgeTo"][destination]
            destination = previous_nodes[destination]

        if shortest_length > curr_length:
            shortest_length = curr_length
            shortest_path= path

    shortest_path.append({
        "bus_stop_name": start,
        "coordinates" : (data[start]["lat"], data[start]["lng"]),
        "bus": data[start]["operating_buses"],
    })

    shortest_path.reverse()
    return (shortest_path,shortest_length)