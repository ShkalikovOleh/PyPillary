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
        '''
        Метод возвращающий кортеж из долготы и широты
        '''
        return (self._longitude, self._latitude)

    
    def __str__(self):
        return str(self._longitude) + "," + str(self._latitude)


class ImageObject:
    '''
    Базовый класс объекта для изображения и последовательности
    '''
    def __init__(self, key, captureDate, userKey, username):
        self._key = key
        self._captureDate = captureDate        
        self._userKey = userKey
        self._username = username


    @property
    def key(self):
        return self._key


    @property
    def captureDate(self):
        return self._captureDate    

    
    @property
    def userKey(self):
        return self._userKey


    @property
    def username(self):
        return self._username


class ImageProperty:
    def __init__(self, imageKey, ca, geoPoint):
        self._geoPoint = geoPoint
        self._key = imageKey
        self._ca = ca


    @property
    def key(self):
        return self._key


    @property
    def geoPoint(self):
        return self._geoPoint


    @property
    def ca(self):
        return self._ca


class Image(ImageObject):
    def __init__(self, imageProperty, captureDate, 
            cameraMake, cameraModel, isPanoram, 
            sequenceKey, userKey, username):
        super().__init__(imageProperty.key, captureDate, userKey, username)
        self._imageProperty = imageProperty
        self._isPanoram = isPanoram
        self._cameraMake = cameraMake
        self._cameraModel = cameraModel        
        self._sequenceKey = sequenceKey        


    def getFilename(self):
        return self._key + ".jpg"


    @property
    def geoPoint(self):
        return self._imageProperty.geoPoint


    @property
    def ca(self):
        return self._imageProperty.ca


    @property
    def cameraMake(self):
        return self._cameraMake


    @property
    def cameraModel(self):
        return self._cameraModel


    @property
    def isPanoram(self):
        return self._isPanoram


    @property
    def sequenceKey(self):
        return self._sequenceKey


class Sequence(ImageObject):
    def __init__(self, key, captureDate, createdDate, imageProperties, userKey, username):
        super().__init__(key, captureDate, userKey, username)
        self._imageProperties = imageProperties
        self._createdDate = createdDate

    
    @property
    def createdDate(self):
        return self._createdDate


    @property
    def imageProperties(self):
        return self._imageProperties