import json
import pandas as pd
from Coordinates import Coordinates
from brain import *


xl = pd.ExcelFile("bus_stops.xlsx")

def generate_excel_overview():
    dict = {}
    for eachNumber in xl.sheet_names:
        data = xl.parse(eachNumber)
        df = pd.DataFrame(data)
        for eachIndex, eachBusStop in df.iterrows():
            gpsCoord = Coordinates(eachBusStop["GPS Location"].split(",")[0].strip(),eachBusStop["GPS Location"].split(",")[1].strip())

            if eachBusStop["Bus stop"] in dict and eachNumber not in dict[eachBusStop["Bus stop"]]["operating_buses"]:
                dict[eachBusStop["Bus stop"]]["operating_buses"]+= [eachNumber]
            else:
                dict[eachBusStop["Bus stop"]] = {
                    "operating_buses":[eachNumber],
                    "lat": gpsCoord.getLat(),
                    "lng": gpsCoord.getLng()
                }

    with open("excel_overview.json", "w") as outfile:
        json.dump(dict, outfile)

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

def collate_datav2():
    dict={}
    for eachBusNumber in xl.sheet_names:
        data = xl.parse(eachBusNumber)
        df = pd.DataFrame(data)
        for eachIndex, currStop in df.iterrows():
            total_len = len(df.index)
            gps_location = currStop["GPS Location"].split(",")
            busStopName = currStop["Bus stop"]
            busNumber = eachBusNumber
            currStopCoord = Coordinates(float(gps_location[0]),float(gps_location[1]))
            edges = []

            # Initialise the data if the busStopName is not in the dictionary
            if busStopName not in dict:
                nearestStop = findNearestStopTest(currStopCoord)
                #nearestStops = findNearest5StopV2(currStopCoord)

                edges.append({
                    nearestStop : distanceBetween(currStopCoord, getCoordFromBusStopName(nearestStop)),
                    "modeOfTransport": ["Walk"]
                })

                # Add data to dictionary
                dict[busStopName] = {
                    "edges": edges,
                }

                dict[busStopName]["lat"] = currStopCoord.getLat()
                dict[busStopName]["lng"] = currStopCoord.getLng()
                dict[busStopName]["operating_buses"] = []
            else:
                # IF the bus stop name already added to the dictioanry
                # Set edges to the existing edges in the dictionary
                edges = dict[busStopName]["edges"] # A List of Dictioanry {busstopname : distance, modeoftransport: list}

                # Add the next stop in the sheet
            if eachIndex + 1 < total_len:
                # Add next stop
                nextStop = df.iloc[eachIndex+1] #Store next stop in a variable for easier access
                nextStopGPS = nextStop["GPS Location"].split(",") # split the coordinates into a list
                nextStopName = nextStop["Bus stop"] # Store bus stop name in a variable
                nextStopCoord = Coordinates(float(nextStopGPS[0]), float(nextStopGPS[1])) # Store coordinate as a class

                cost = distanceBetween(currStopCoord, nextStopCoord) #Cost of initial stop to nextStop
                busExist = False

                for eachExistingEdges in edges:
                    if nextStopName in eachExistingEdges:
                        if cost == eachExistingEdges[nextStopName]:
                            print("Exists")
                            busExist= True
                            eachExistingEdges["modeOfTransport"].append(busNumber)

                if not busExist:
                    print("No exists")
                    edges.append({
                        nextStopName: distanceBetween(currStopCoord, nextStopCoord),
                        "modeOfTransport" : [eachBusNumber]
                    })



            dict[busStopName]["edges"] = edges
            if busNumber not in dict[busStopName]["operating_buses"]:
                dict[busStopName]["operating_buses"].append(busNumber)


    with open("collated_datav2.json", "w") as outfile:
        json.dump(dict, outfile)

#collate_datav2()
#print(reader("Opp Shell Kiosk @ Taman Sri Putri"))
#collate_data()
#generate_excel_overview()
