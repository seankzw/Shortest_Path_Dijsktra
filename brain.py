import json
import geocoder
from math import radians, cos, sin, asin, sqrt

from Coordinates import Coordinates

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
