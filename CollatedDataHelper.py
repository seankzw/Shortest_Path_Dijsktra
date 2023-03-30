import json
from Coordinates import Coordinates

from brain import getCollatedData
class CollatedDataHelper:
    def __init__(self):
        f = open("collated_data.json")
        self.data = json.load(f)

    def getBusStop(self,bus_stop_name):
        return self.data[bus_stop_name]

    def getEdgesFromBusStop(self, bus_stop_name):
        return self.data[bus_stop_name]["edgeTo"]

    def getBusNumberFromBusStop(self, bus_stop_name):
        return self.data[bus_stop_name]["bus_number"]

    def getCoordFromBusStopName(busStopName):
        data = getCollatedData()
        coord = Coordinates(data[busStopName]["lat"], data[busStopName]["lng"])
        return coord


