class Coordinates:
    def __init__(self,lat,lng):
        self.lat = lat
        self.lng = lng

    def getLat(self):
        return float(self.lat)

    def getLng(self):
        return float(self.lng)

    def setLat(self, lat):
        self.lat = lat;

    def setLng(self, lng):
        self.lng = lng
