from collections import deque
import json
import sys
import geocoder
from math import radians, cos, sin, asin, sqrt

from Coordinates import Coordinates
#from main import getOverviewData

def distanceBetween(currLoc, userLoc):

    # The math module contains a function named
	# radians which converts from degrees to radians.
	lat1 = radians(currLoc.getLat())
	lon1 = radians(currLoc.getLng())

	lat2 = radians(userLoc.getLat())
	lon2 = radians(userLoc.getLng())

	# Haversine formula
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

	c = 2 * asin(sqrt(a))

	# Radius of earth in kilometers. Use 3956 for miles
	r = 6371

	# calculate the result
	return(c * r)

# Find nearest location to busstop from User Location
def findNearestStop(userLoc):
	f = open("excel_overview.json")
	data = json.load(f)

	shortestDistance = 1000
	for i in data:
		dataCoord = Coordinates(data[i]["lat"],data[i]["lng"])
		if distanceBetween(dataCoord, userLoc) < shortestDistance:
			shortestDistance = distanceBetween(dataCoord ,userLoc)
			index = i

	startBus = index
	return (startBus)

# Find nearest location to busstop from User Location
def findNearestStopWithData(userLoc, data):
	shortestDistance = 1000
	for i in data:
		dataCoord = Coordinates(data[i]["lat"],data[i]["lng"])
		if distanceBetween(dataCoord, userLoc) < shortestDistance:
			shortestDistance = distanceBetween(dataCoord ,userLoc)
			index = i
	startBus = index
	return startBus

def findNearest5Stop(userLoc):
	f = open("excel_overview.json")
	all_bus_stops = json.load(f)
	counter = 0
	shortest5=[]

	while counter < 5:
		nearest_stop = findNearestStopWithData(userLoc, all_bus_stops)
		shortest5.append(nearest_stop)
		del all_bus_stops[nearest_stop]
		counter +=1

	return shortest5

def getCoordFromBusStopName(busStopName):
	data = getOverviewData()
	coord = Coordinates(data[busStopName]["lat"], data[busStopName]["lng"])
	return coord


def userLocation():
	# User Location
	g = geocoder.ip('me')
	userLoc = g.latlng
	print(userLoc)

def getBoundingBox(loc1, loc2):
	x1 = loc1[0]
	y1 = loc1[1]
	x2 = loc2[0]
	y2 = loc2[1]

	topLeftX = max(x1,x2)
	topLeftY = min(y1,y2)
	botRightX = min(x1,x2)
	botRightY = max(y1,y2)

	return (topLeftX, topLeftY),(botRightX, botRightY)
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
    collated_data = getCollatedData()

    while destination != start:
        path.append({
            "bus_stop_name": destination,
            "coordinates" : (data[destination]["lat"], data[destination]["lng"]),
            "bus": data[destination]["operating_buses"]
        })

        prev_dest = previous_nodes[destination]
        curr_length+= collated_data[prev_dest]["edgeTo"][destination]
        destination = previous_nodes[destination]

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


def getShortestPathFromList(previous_nodes, start, end_stops, toReach):
    data = getOverviewData()
    collated_data = getCollatedData()
    shortest_path = []
    shortest_length = float('inf')
    distance_to_end = float('inf')

    for i in range(len(end_stops)):
        destination = end_stops[i]
        curr_length = 0
        path = []
        eachDestCoord = Coordinates(data[destination]["lat"], data[destination]["lng"])
        while destination != start:
            path.append({
                "bus_stop_name": destination,
                "coordinates" : (data[destination]["lat"], data[destination]["lng"]),
                "bus": data[destination]["operating_buses"]
            })

            prev_dest = previous_nodes[destination]
            curr_length+= collated_data[prev_dest]["edgeTo"][destination]
            destination = previous_nodes[destination]

        if shortest_length > curr_length or distanceBetween(eachDestCoord, toReach) < distance_to_end:
            shortest_length = curr_length
            #print("getShotrtestPathFromList method; eachDestCoord = {}, toReach = {}".format(eachDestCoord, toReach))
            distance_to_end = distanceBetween(eachDestCoord, toReach)
            shortest_path= path

    shortest_path.append({
        "bus_stop_name": start,
        "coordinates" : (data[start]["lat"], data[start]["lng"]),
        "bus": data[start]["operating_buses"],
    })

    shortest_path.reverse()
    return (shortest_path,shortest_length)

def getLeastTransferFromList(previous_nodes, start, end_stops, toReach):
    data = getOverviewData()
    collated_data = getCollatedData()
    shortest_path = []
    shortest_length = float('inf')
    distance_to_end = float('inf')

    for i in range(len(end_stops)):
        destination = end_stops[i]
        curr_length = 0
        path = []
        visited = set()
        eachDestCoord = Coordinates(data[destination]["lat"], data[destination]["lng"])
        while destination != start:
            path.append({
                "bus_stop_name": destination,
                "coordinates" : (data[destination]["lat"], data[destination]["lng"]),
                "bus": data[destination]["operating_buses"]
            })

            prev_dest = previous_nodes[destination]
            curr_length+= collated_data[prev_dest]["edgeTo"][destination]
            destination = previous_nodes[destination]

        if shortest_length > curr_length or distanceBetween(eachDestCoord, toReach) < distance_to_end:
            shortest_length = curr_length
            #print("getShotrtestPathFromList method; eachDestCoord = {}, toReach = {}".format(eachDestCoord, toReach))
            distance_to_end = distanceBetween(eachDestCoord, toReach)
            shortest_path= path

    shortest_path.append({
        "bus_stop_name": start,
        "coordinates" : (data[start]["lat"], data[start]["lng"]),
        "bus": data[start]["operating_buses"],
    })

    shortest_path.reverse()
    return (shortest_path,shortest_length)

def getTimeTaken(distance, speed):
    return distance / speed
    

def getAmountOfTrf(path):
    for i in path:
         print(i["bus"])
         print("---")

