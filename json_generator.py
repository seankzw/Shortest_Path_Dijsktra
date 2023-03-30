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

def collate_data():
    dict={}
    for eachBusNumber in xl.sheet_names:
        data = xl.parse(eachBusNumber)
        df = pd.DataFrame(data)
        for eachIndex, currStop in df.iterrows():
            total_len = len(df.index)
            gps_location = currStop["GPS Location"].split(",")
            currStopCoord = Coordinates(float(gps_location[0]),float(gps_location[1]))
            destination = {}
            curr_bus_number = []


            if eachIndex + 1 < total_len:
                # Add next stop
                nextStop = df.iloc[eachIndex+1]
                nextStopGPS = nextStop["GPS Location"].split(",")
                nextStopCoord = Coordinates(float(nextStopGPS[0]), float(nextStopGPS[1]))

                if nextStop["Bus stop"] not in destination:
                    destination[nextStop["Bus stop"]] = distanceBetween(currStopCoord,nextStopCoord)

                #newDestination = {
                #        "bus_stop": nextStop["Bus stop"],
                #        "distance":distanceBetween(currStopCoord,nextStopCoord)
                #}


            if eachBusNumber not in curr_bus_number:
                curr_bus_number.append(eachBusNumber)

            dict[currStop["Bus stop"]] = {
                "bus_number": curr_bus_number,
                "edgeTo":destination
            }

    with open("collated_data.json", "w") as outfile:
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

            # Initialise the data
            if busStopName not in dict:
                #nearestStop = findNearestStopTest(currStopCoord)
                nearestStops = findNearest5StopV2(currStopCoord)

                for i in range(len(nearestStops)):
                    print(nearestStops[i])
                    edges.append({
                        nearestStops[i] : distanceBetween(currStopCoord, getCoordFromBusStopName(nearestStops[i])),
                        "modeOfTransport": "Walk"
                    })
                dict[busStopName] = {
                    "edges": edges
                }
            else:
                edges = dict[busStopName]["edges"]

            # Add the next stop in the sheet
            if eachIndex + 1 < total_len:
                # Add next stop
                nextStop = df.iloc[eachIndex+1]
                nextStopGPS = nextStop["GPS Location"].split(",")
                nextStopName = nextStop["Bus stop"]
                nextStopCoord = Coordinates(float(nextStopGPS[0]), float(nextStopGPS[1]))
                edges.append({
                    nextStopName: distanceBetween(currStopCoord, nextStopCoord),
                    "modeOfTransport" : eachBusNumber
                })




            # "Larkin Terminal": {
            #   "edges": [
            #       {
            #           "Perjabad ..": 0.6,
            #           "modeOfTransport": "Walk"
            #       },
            #       {
            #           "nextBusStop..": 0.6,
            #           "modeOfTransport": "P411"
            #       },
            #       {
            #           "nextBusStop..": 0.6,
            #           "modeOfTransport": "P101"
            #       }
            #   ]
            # }




            #nearestBusStop = findNearestStopTest(currStopCoord)
            #destination[nearestBusStop] = distanceBetween(currStopCoord, getCoordFromBusStopName(nearestBusStop))
            #curr_bus_number.append("Walk")


            #if eachIndex + 1 < total_len:
            #    # Add next stop
            #    nextStop = df.iloc[eachIndex+1]
            #    nextStopGPS = nextStop["GPS Location"].split(",")
            #    nextStopCoord = Coordinates(float(nextStopGPS[0]), float(nextStopGPS[1]))

            #    if nextStop["Bus stop"] not in destination:
            #        destination[nextStop["Bus stop"]] = distanceBetween(currStopCoord,nextStopCoord)



            #    #newDestination = {
            #    #        "bus_stop": nextStop["Bus stop"],
            #    #        "distance":distanceBetween(currStopCoord,nextStopCoord)
            #    #}

            #if eachBusNumber not in curr_bus_number:
            #    curr_bus_number.append(eachBusNumber)

            dict[currStop["Bus stop"]]["edges"] = edges

            #dict[currStop["Bus stop"]] = {
            #    "bus_number": curr_bus_number,
            #    "edgeTo": destination
            #}

    with open("collated_datav2.json", "w") as outfile:
        json.dump(dict, outfile)

collate_datav2()
#print(reader("Opp Shell Kiosk @ Taman Sri Putri"))
#collate_data()
#generate_excel_overview()
