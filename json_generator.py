import json
import pandas as pd
from Coordinates import Coordinates
from brain import distanceBetween

xl = pd.ExcelFile("bus_stops.xlsx")


def collate_data():
    dict={}

#    for eachBusNumber in xl.sheet_names:
#        eachBusRoute = xl.parse(eachBusNumber)
#        df = pd.DataFrame(eachBusRoute)
#        currIndex = 0
    for eachBusNumber in xl.sheet_names:
        data = xl.parse(eachBusNumber)
        df = pd.DataFrame(data)
        for eachIndex, currStop in df.iterrows():
            total_len = len(df.index)
            gps_location = currStop["GPS Location"].split(",")
            currStopCoord = Coordinates(float(gps_location[0]),float(gps_location[1]))
            destination = []
            curr_bus_number = []

            if currStop["Bus stop"] in dict:
                curr_bus_number = dict[currStop["Bus stop"]]["bus_number"]
                destination = dict[currStop["Bus stop"]]["destination"]


            if eachIndex + 1 < total_len:
                # Add next stop
                nextStop = df.iloc[eachIndex+1]
                nextStopGPS = nextStop["GPS Location"].split(",")
                nextStopCoord = Coordinates(float(nextStopGPS[0]), float(nextStopGPS[1]))

                newDestination = {
                        "bus_stop": nextStop["Bus stop"],
                        "distance":distanceBetween(currStopCoord,nextStopCoord)
                }

                if newDestination not in destination:
                    destination.append(newDestination)

            if eachBusNumber not in curr_bus_number:
                curr_bus_number.append(eachBusNumber)

            dict[currStop["Bus stop"]] = {
                "bus_number": curr_bus_number,
                "destination":destination
            }

    with open("collated_data.json", "w") as outfile:
        json.dump(dict, outfile)

#    dict = {}

#    for eachBusNumber in xl.sheet_names:
#        eachBusRoute = xl.parse(eachBusNumber)
#        df = pd.DataFrame(eachBusRoute)
#        currIndex = 0
#        for index, row in df.iterrows():
#            coordinatesOfBusStop = Coordinates(float(row["GPS Location"].split(",")[0]),float(row["GPS Location"].split(",")[1]))
#            if row["Bus stop"] not in dict:
#                coordinateOfNextBusStop = Coordinates(float(df.iloc[currIndex+1]["GPS Location"].split(",")[0]),float(df.iloc[currIndex+1]["GPS Location"].split(",")[1]))
#                dict[row["Bus stop"]] = {
#                    "bus_number": [eachBusNumber],
#                    "destination":[
#                        {
#                            "bus_stop":df.iloc[currIndex+1]["Bus stop"],
#                            "distance": distanceBetween(coordinatesOfBusStop, coordinateOfNextBusStop)
#                        }
#                    ]
#                }

#            currIndex+=1


#    with open("collated_data.json", "w") as outfile:
#        json.dump(dict, outfile)


def generateSourcetoDestination():
    f = open("collated_data.json")
    data = json.load(f)

    newDict = {}

    for i in data:
        currCoord = Coordinates(data[i]["lat"], data[i]["lng"])
        temp = {}
        for j in data:
            nextCoord = Coordinates(data[j]["lat"], data[j]["lng"])
            if j != i:
                if checkBusExists(data[i]["buses"], data[j]["buses"]):
                    temp.update({
                         j: distanceBetween(currCoord, nextCoord)
                    })

        newDict[i] = temp

    print("len = {}".format(len(newDict)))
    with open("source_to_destination.json", "w") as outfile:
        json.dump(newDict, outfile)

def checkBusExists(locationA, locationB):
    print(locationA, locationB)
    for i in range(len(locationA)):
        if locationA[i] in locationB:
            print("locationA in locationB")
            return True

    print('======')
    return False


def test():
    df = pd.read_csv("bus_routes.csv")
    mainDict = {}
    for idx, row in df.iterrows():
        if  row["source"] not in mainDict:
            mainDict[row["source"]] = {}

        mainDict[row["source"]][row["destination"]] = row["distance"]
        #if shortestRoute > row["distance"] :
        #    name = row["destination"]

    df = pd.DataFrame(mainDict)
    with open("test.json","w") as outfile:
        json.dump(mainDict, outfile)
        #    shortestRoute = row["distance"]

    #print(mainDict)

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


def busExists(a,b):
    res = True
    for i in range(len(a)):
        if a[i] not in b:
           res = False
    return res

#print(reader("Opp Shell Kiosk @ Taman Sri Putri"))

#generateSourcetoDestination()
collate_data()
