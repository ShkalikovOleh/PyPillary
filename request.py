import model
import requests
from queue import Queue
from dateutil.parser import parse
from threading import Thread

sequencePrefix = "sequences"
andPart = "&"
answerPart = "?"
comaPart = ","


class APIRequest:
    _apiPrefix = "https://a.mapillary.com/v3/"
    
    def __init__(self, clientId, clientSecret):
        self._clientId = clientId
        self._clientSecret = clientSecret
        self._requestString = ""

    @property
    def requestString(self):
        return self._requestString


    @property
    def response(self):
        return self._response


    def checkAnd(self):
        if self._requestString[-1] != '/' and self._requestString[-1] != '&':        
            self._requestString += andPart


    def get(self):
        self.checkAnd()
        self._requestString += ("client_id=" + self._clientId)
        self._response = requests.get(self._requestString)
        return self._response


class ImageRequest(APIRequest):    
    _imagePrefix = "images"    

    def search(self):
        self._requestString += (self._apiPrefix + self._imagePrefix + answerPart)
        isr = ImageSearchRequest(self._clientId, self._clientSecret)
        isr._requestString = self._requestString
        return isr


    def download(self, image, resolution, dirPath, threadCount = 1):        
        return ImageDownloadRequest(self._clientId, self._clientSecret, image, resolution, dirPath, threadCount)


class ImageSearchRequest(APIRequest):
    def addBbox(self, geoPointMin, geoPointMax):
        self.checkAnd()
        self._requestString += ("bbox=" + str(geoPointMin.longitude) + comaPart + 
            str(geoPointMin.latitude) + comaPart + str(geoPointMax.longitude) + 
            comaPart + str(geoPointMax.latitude))
        return self


    def addStartTime(self, datetime):
        '''
        param datetime is datatime type object
        '''
        self.checkAnd()
        self._requestString += ("start_time=" + datetime.isoformat())
        return self    


    def addEndTime(self, datetime):
        '''
        param datetime is datatime type object
        '''
        self.checkAnd()
        self._requestString += ("end_time=" + datetime.isoformat())
        return self


    def get(self):
        super().get()
        images = []
        for feature in self._response.json()['features']:
            properties = feature['properties']
            geometry = feature['geometry']

            geoPoint = model.GeoPoint(geometry['coordinates'][0], geometry['coordinates'][1])
            image = model.Image(geoPoint, key = properties['key'], 
                date = parse(properties['captured_at']), ca = properties['ca'],
                cameraMake = properties['camera_make'], cameraModel = properties['camera_model'],
                sequenceKey = properties['sequence_key'], isPanoram = properties['pano'],
                userKey = properties['user_key'], username = properties['username'])
            
            images.append(image)
        return images


class ImageDownloadRequest(APIRequest):
    _cdnPrefix = "https://d1cuyjsrcm0gby.cloudfront.net/"
    _imageResolutions = {320: "/thumb-320.jpg",
                    640: "/thumb-640.jpg",
                    1024: "/thumb-1024.jpg",
                    2048: "/thumb-2048.jpg"}

    def __init__(self, clientId, clientSecret, images, resolution, dirPath, threadCount):
        super().__init__(clientId, clientSecret)        
        self._resolution = resolution
        self._threadCount = threadCount
        self._dirPath = dirPath
        self._images = images


    def get(self):
        def download(imagesQueue, resolution, dirPath):
            while not imagesQueue.empty():
                image = imagesQueue.get()
                with open(dirPath + image.getFilename(), "wb") as file:
                    response = requests.get(ImageDownloadRequest._cdnPrefix + 
                        image.key + ImageDownloadRequest._imageResolutions[resolution])
                    file.write(response.content)            

        queue = Queue()
        if isinstance(self._images, model.Image):
            queue.put(self._images)
            download(queue, self._resolution, self._dirPath)
        elif isinstance(self._images, list):            
            for img in self._images:
                queue.put(img)
            threads = []
            for i in range(self._threadCount):
                thread = Thread(target = download, args=(queue, self._resolution, self._dirPath))
                thread.start()                
            


class APIService:
    def __init__(self, credPath):
        with open(credPath, "r") as file:
            self._clientId = file.readline().replace("\n", "") 
            self._clientSecret = file.readline().replace("\n", "")


    def createImageRequest(self):
        return ImageRequest(self._clientId, self._clientSecret)

    
    def createCustomRequest(self, requestString):
        request = APIRequest(self._clientId, self._clientSecret)
        request._requestString = request._apiPrefix + requestString
        return request