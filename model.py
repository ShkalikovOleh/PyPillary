class GeoPoint:    
    def __init__(self, longitude,latitude):
        self._longitude = longitude
        self._latitude = latitude


    @property
    def longitude(self):
        return self._longitude


    @property
    def latitude(self):
        return self._latitude


    @property
    def coordinates(self):
        return (self._longitude, self._latitude)


class Image:
    def __init__(self, geoPoint, key, date, 
        ca, cameraMake, cameraModel, isPanoram, 
        sequenceKey, userKey, username):
        
        self._geoPoint = geoPoint
        self._key = key
        self._date = date
        self._ca = ca
        self._cameraMake = cameraMake
        self._cameraModel = cameraModel
        self._isPanoram = isPanoram
        self._sequenceKey = sequenceKey
        self._userKey = userKey
        self._username = username        


    def getFilename(self):
        return self._key + ".jpg"

    @property
    def geoPoint(self):
        return self._geoPoint


    @property
    def key(self):
        return self._key


    @property
    def date(self):
        return self._date


    @property
    def ca(self):
        return self._ca


    @property
    def cameraMake(self):
        return self._cameraMake

        
    @property
    def cameraMake(self):
        return self._cameraModel


    @property
    def isPanoram(self):
        return self._isPanoram

        
    @property
    def sequenceKey(self):
        return self._sequenceKey

        
    @property
    def userKey(self):
        return self._userKey


    @property
    def username(self):
        return self._username