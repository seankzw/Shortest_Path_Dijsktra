import json
import geocoder
from math import radians, cos, sin, asin, sqrt

def distance(lat1, lat2, lon1, lon2):

    # The math module contains a function named
	# radians which converts from degrees to radians.
	lon1 = radians(lon1)
	lon2 = radians(lon2)
	lat1 = radians(lat1)
	lat2 = radians(lat2)

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
def findStartBus(userLoc):
    # try:
	f = open("bus_route.json")
	data = json.load(f)

	shortestDistance = 1000
	minLat = 10000
	minLng = 100000
	for i in data:
		#if distance(data[i]["lat"], userLoc[0], data[i]["lng"], userLoc[1])< shortestDistance:
		if distance(data[i]["lat"], userLoc.getLat(), data[i]["lng"], userLoc.getLng())< shortestDistance:
			minLat = data[i]["lat"]
			minLng = data[i]["lng"]
			shortestDistance = distance(data[i]["lat"], userLoc.getLat(), data[i]["lng"], userLoc.getLng())
			index = i

		# if data[i]["coordinates"][0] < minLat : minLat = data[i]["coordinates"][0]
		# if data[i]["coordinates"][1] < minLng : minLng = data[i]["coordinates"][1]
	# return min(data, key=lambda p: distance(userLoc[0],p['coordinates',[0]],userLoc[1],p['coordinates',[1]]))
	startBus = index
	print (startBus)
	print(minLat, minLng)
	print("Distance = ", round(shortestDistance) , "km")
	return (startBus)

	# except TypeError:
		# print('Not a list or not a number.')

# Location closest to End Location (TEST)


# Function Test

# Taking in coordinates of busstops
#print(data)

# User Location
g = geocoder.ip('me')
userLoc = g.latlng
print(userLoc)

# Nearest busstop to user
#print("The nearest busstop is " + findStartBus(data, userLoc))
# print(data['coordinates',[0]])