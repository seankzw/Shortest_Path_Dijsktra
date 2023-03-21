from Coordinates import Coordinates
from brain import findNearest5Stop, findNearestStop
from main import dijkstra, getShortestPath, getShortestPathFromList

paradigm_mall = Coordinates(1.514813892563429,103.6852375606564)
larkin_terminal = Coordinates(1.4964559999542668,103.74374661113058)

def oldAlgoTestCase():
    end_bus_stop= findNearestStop(paradigm_mall)
    start_node= findNearestStop(larkin_terminal)
    previous_node, shortest_path = dijkstra(start_node)
    path = getShortestPath(previous_node, shortest_path, start_node, end_bus_stop)
    printPath(path)

def newAlgoTestCase():
    start_node= findNearestStop(larkin_terminal)
    previous_node, shortest_path = dijkstra(start_node)
    end_bus_stops = findNearest5Stop(paradigm_mall)
    path2, length = getShortestPathFromList(previous_node, start_node, end_bus_stops)
    printPath(path2)


def printPath(path):
    for i in path:
        print(i["bus_stop_name"], "->")

