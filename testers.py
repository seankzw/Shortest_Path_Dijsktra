from brain import *

overview_data = getCollatedData()
paradigm_mall = Coordinates(1.514813892563429,103.6852375606564)
larkin_terminal = Coordinates(1.4964559999542668,103.74374661113058)
johor_islamic_complex = Coordinates(overview_data["Johor Islamic Complex"]["lat"], overview_data["Johor Islamic Complex"]["lng"])

def newAlgoTestCase():
    start_node= findNearestStop(johor_islamic_complex)
    previous_node, shortest_path = dijkstra(start_node)
    end_bus_stops = findNearest5Stop(larkin_terminal)
    print(end_bus_stops)
    path2, length = getShortestPathFromList(previous_node, start_node, end_bus_stops, larkin_terminal)
    printPath(path2)


def printPath(path):
    for i in path:
        print(i["bus_stop_name"], "->")

def getAmountOfTransfer():
    start_node= findNearestStop(johor_islamic_complex)
    previous_node, shortest_path = dijkstra(start_node)
    end_bus_stops = findNearest5Stop(paradigm_mall)
    path2, length = getShortestPathFromList(previous_node, start_node, end_bus_stops, larkin_terminal)
    getAmountOfTrf(path2)

def newestAlgo():
    kampung_melayu_kulai = Coordinates(1.6616744, 103.5975579)
    start_node = findNearestStop(kampung_melayu_kulai)
    senai_airpot = Coordinates(1.6359642, 103.66680084847599)
    end_bus_stops = findNearest5Stop(senai_airpot)
    previous_node, shortestPath= dijkstra(start_node)
    #print(end_bus_stops)
    path , length= getShortestPathFromList(previous_node, start_node, end_bus_stops, senai_airpot)
    for i in range(len(path)):
        print("Go to {} via {}".format(path[i]["bus_stop_name"], path[i]["bus"]))
    print("Length = {}".format(length))


newestAlgo()
