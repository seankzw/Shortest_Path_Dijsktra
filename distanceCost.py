from geopy import distance
import json

# Taking in coordinates of busstops
f = open("data.json")
data = json.load(f)
#print(data)
    
location1 = (1.4964559999542668, 103.74374661113058)
location2 = (1.491850778809332, 103.740872550932728)
print(distance.distance(location1, location2).km)


