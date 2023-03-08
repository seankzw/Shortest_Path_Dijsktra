import json
import pandas as pd
from Coordinates import Coordinates
from brain import distanceBetween

xl = pd.ExcelFile("bus_stops.xlsx")


def generateBusDict():
    listOfBus = xl.sheet_names
    with open("bus_number.py", "w") as outfile:
        json.dump(listOfBus, outfile)


def collate_data():
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

    with open("collated_data.json", "w") as outfile:
        json.dump(dict, outfile)


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
    for i in range(len(locationA)):
        if locationA[i] in locationB:
            return True

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
#test2()
#test()
#generateNearestStop()
#generateBusDict()
#generateRoutesDict()

generateSourcetoDestination()
#collate_data()
