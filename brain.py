from collections import deque
import json
import sys
import geocoder
from math import radians, cos, sin, asin, sqrt

from Coordinates import Coordinates
#from main import getOverviewData

def isSameCoord(coordinate1, coordinate2):
    return coordinate1.getLat() == coordinate2.getLat() and coordinate1.getLng() == coordinate2.getLng()

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
def findNearestStopTest(userLoc):
    f = open("excel_overview.json")
    data = json.load(f)
    index = ""
    shortestDistance = 1000
    for i in data:
        dataCoord = Coordinates(data[i]["lat"],data[i]["lng"])
        #print(dataCoord, userLoc , " It IS {}".format(dataCoord == userLoc))
        if(distanceBetween(dataCoord, userLoc) < shortestDistance) and not isSameCoord(userLoc, dataCoord):
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
    f = open("collated_datav2.json")
    data = json.loads(f.read())
    return data

def getOverviewData():
    f = open("excel_overview.json")
    data = json.loads(f.read())
    return data

def getBusTiming():
     f = open("bus_timings.json")
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
        edges = data[curr_shortest_route]["edges"]
        # for eachDestination in edges:
        for eachDestination in edges:
            for index, (destination, distanceCost) in enumerate(eachDestination.items()):
                if index == 0:
                    tent_val = shortest_path[curr_shortest_route] + distanceCost
            # tent_val = shortest_path[curr_shortest_route] + data[curr_shortest_route]["edgeTo"][eachDestination]
            #print("Unvisited node = {}".format(unvisited_nodes))
                    if tent_val < shortest_path[destination]:
                        shortest_path[destination] = tent_val
                        previous_nodes[destination] = curr_shortest_route


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

    print(end_stops)
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
            edges = collated_data[prev_dest]["edges"]
            shortestCost = 0
            for eachEdgesIndex in range (len(edges)):
                if eachEdgesIndex == 0:
                    for index, (destinationName, distanceCost) in enumerate(edges[eachEdgesIndex].items()):
                        if index == 0:
                            shortestCost = distanceCost
                else:
                    for index, (destinationName, distanceCost) in enumerate(edges[eachEdgesIndex].items()):
                        if index == 0 and distanceCost < shortestCost:
                            shortestCost = distanceCost
                        
            curr_length+= shortestCost
            destination = previous_nodes[destination]

        if shortest_length > curr_length and distanceBetween(eachDestCoord, toReach) < distance_to_end:
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

def TimeFormatter(totalTime):
    # totalTime will be in hours since speed is in km/h and distance is in km
    # converting hours to seconds
    totalTime *= 3600
    # from seconds, convert to hours, minutes and seconds (if needed)
    hours = int(totalTime // 3600) # getting the hours 
    seconds = totalTime % 3600
    minutes = int(seconds // 60) # getting the minutes
    seconds %= 60 # getting the seconds

    timeFormatter = "" # a string format for the time

    if hours != 0:
        if hours > 1:
            timeFormatter += str(hours) + " hrs "
        else:
            timeFormatter += str(hours) + " hr "

    if minutes != 0:
        if minutes > 1:
            timeFormatter += str(minutes) + " mins"
        else:
            timeFormatter += str(minutes) + " min"

    return timeFormatter

def getAmountOfTrf(path):
    for i in path:
         print(i["bus"])
         print("---")

#! ================= NEW VERSION =============================

def findNearestStopWithDatav2(userLoc, data):
    shortestDistance = 1000
    for i in data:
        dataCoord = Coordinates(data[i]["lat"],data[i]["lng"])
        if(distanceBetween(dataCoord, userLoc) < shortestDistance) and not isSameCoord(userLoc, dataCoord):
            shortestDistance = distanceBetween(dataCoord ,userLoc)
            index = i
    startBus = index
    return startBus

def findNearest5StopV2(userLoc):
	f = open("excel_overview.json")
	all_bus_stops = json.load(f)
	counter = 0
	shortest5=[]

	while counter < 5:
		nearest_stop = findNearestStopWithDatav2(userLoc, all_bus_stops)
		shortest5.append(nearest_stop)
		del all_bus_stops[nearest_stop]
		counter +=1

	return shortest5

# Find nearest location to busstop from User Location
def findNearestStopV2(userLoc):
    f = open("excel_overview.json")
    data = json.load(f)
    index = ""
    shortestDistance = 1000
    for i in data:
        dataCoord = Coordinates(data[i]["lat"],data[i]["lng"])
        #print(dataCoord, userLoc , " It IS {}".format(dataCoord == userLoc))
        if(distanceBetween(dataCoord, userLoc) < shortestDistance) and not isSameCoord(userLoc, dataCoord):
            shortestDistance = distanceBetween(dataCoord ,userLoc)
            index = i

    startBus = index
    return (startBus)