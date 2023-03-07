import json
import pandas as pd
from Coordinates import Coordinates
from brain import distanceBetween



xl = pd.ExcelFile("bus_stops.xlsx")


def generateBusDict():
    listOfBus = xl.sheet_names
    with open("bus_number.py", "w") as outfile:
        json.dump(listOfBus, outfile)


def generateRoutesDict():
    dict = {}
    for eachSheetIdx in range(len(xl.sheet_names)):
        sheetName = xl.sheet_names[eachSheetIdx]
        eachSheetData = xl.parse(sheetName)
        df = pd.DataFrame(eachSheetData)
        for index, row in df.iterrows():
            location = row["GPS Location"]
            coordinatesVal = (0,0)
            if location != "NIL":
                coordinatesVal = (float(location.split(",")[0]), float(location.split(",")[1]))

            if row["Bus stop"] not in dict:
                dict[row["Bus stop"]] = {
                    "buses" : [sheetName],
                    "lat": coordinatesVal[0],
                    "lng": coordinatesVal[1]

                }
            else:
                if sheetName not in dict[row["Bus stop"]]["buses"]:
                    dict[row["Bus stop"]]["buses"] += [sheetName]

    with open("bus_route.json", "w") as outfile:
        json.dump(dict, outfile)

def busExists(a,b):
    res = True
    for i in range(len(a)):
        if a[i] not in b:
           res = False
    return res

def generateNearestStop():
    f = open("bus_route.json")
    data = json.load(f)

    newDict = {
        'source': [],
        'destination':[],
        'distance':[]
    }

    for i in data:
        currDataCoord = Coordinates(data[i]["lat"], data[i]["lng"])
        for j in data:
            nextDataCoord = Coordinates(data[j]["lat"], data[j]["lng"])
            if(distanceBetween(currDataCoord, nextDataCoord) != 0):
                #if busExists(data[i]["buses"], data[j]["buses"]):
                newDict["source"].append(i)
                newDict["destination"].append(j)
                newDict["distance"].append(distanceBetween(currDataCoord, nextDataCoord))


    df = pd.DataFrame(newDict)
    df.to_csv("bus_routes.csv")
    #with open("nearest_stops.json", "w") as outfile:
    #    json.dump(newDict, outfile)


def reader(source):
    df = pd.read_csv("bus_routes.csv")

    name = ""
    shortestRoute = 10000000

    newDf = df[(df.source == source)]

    for index, row in newDf.iterrows():
        if shortestRoute > row["distance"] :
            name = row["destination"]
            shortestRoute = row["distance"]

    return ("Shorterst stop from {} is {} at {}km".format(source, name, shortestRoute))

print(reader("Opp Shell Kiosk @ Taman Sri Putri"))
#generateNearestStop()
#generateBusDict()
#generateRoutesDict()

