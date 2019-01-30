class GeoPoint:    
    def __init__(longitude,latitude):
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
        self._cameraModel = camera_model
        self._isPanoram = isPanoram
        self._sequenceKey = sequenceKey
        self._userKey = userKey
        self._username = username        


    def getFilename():
        return self._key + ".jpg"

    @property
    def geoPoint():
        return self._geoPoint


    @property
    def key():
        return self.key


    @property
    def date():
        return self._date


    @property
    def ca():
        return self._ca


    @property
    def cameraMake():
        return self._cameraMake

        
    @property
    def cameraMake():
        return self._cameraModel


    @property
    def isPanoram():
        return self._isPanoram

        
    @property
    def sequenceKey():
        return self._sequenceKey

        
    @property
    def userKey():
        return self._userKey


    @property
    def username():
        return self._username