import pypillary.model as model
import aiohttp
import asyncio
from queue import Queue
from dateutil.parser import parse
from threading import Thread
import os

andPart = "&"
answerPart = "?"
comaPart = ","
slehPart = "/"


class APIRequest:
    _apiPrefix = "https://a.mapillary.com/v3/"

    def __init__(self, clientId, clientSecret):
        self._clientId = clientId
        self._clientSecret = clientSecret
        self._requestString = APIRequest._apiPrefix
        self._response = []

    @property
    def requestString(self):
        return self._requestString

    @property
    def response(self):
        return self._response

    def checkAnd(self):
        if self._requestString[-1] != '/' and self._requestString[-1] != '&':
            self._requestString += andPart

    async def execute(self, session):
        if answerPart in self._requestString:
            self.checkAnd()
        else:
            self._requestString += answerPart
        self._requestString += ("client_id=" + self._clientId)

        async def requestAsync(url):
            async with session.get(self._requestString) as response:
                json = await response.json()
                return json, response.links

        json, links = await requestAsync(self._requestString)
        self._response.append(json)
        while 'next' in links:
            json, links = await requestAsync(links['next']['url'])
            self._response.append(json)
        return self._response    


class ImageObjectSearchRequest(APIRequest):

    def addBbox(self, geoPointMin, geoPointMax):
        self.checkAnd()
        self._requestString += ("bbox=" + str(geoPointMin) + comaPart + str(geoPointMax))
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

    def addUserkeys(self, userkeysList):
        self.checkAnd()
        self._requestString += "userkeys="
        for key in userkeysList:
            self._requestString += (key + comaPart)
        self._requestString = self._requestString[:-1]
        return self

    def addUsenames(self, usernamesList):
        self.checkAnd()
        self._requestString += "usernames="
        for name in usernamesList:
            self._requestString += (name + comaPart)
        self._requestString = self._requestString[:-1]
        return self

    def addPerPage(self, countPerPage):
        self.checkAnd()
        self._requestString += ("per_page=" + str(countPerPage))
        return self

    def parseSearchResponse(self, json):
        raise NotImplementedError()

    async def execute(self, session):
        await super().execute(session)
        items = []
        for response in self._response:
            items.extend(self.parseSearchResponse(response))
        self._response = items
        return self._response


class ImageRequest(APIRequest):
    _imagePrefix = "images"

    def __init__(self, clientId, clientSecret, key):
        super().__init__(clientId, clientSecret)
        self._requestString += (self._imagePrefix + slehPart + key)

    def checkSleh(self):
        if self._requestString[-1] == slehPart:
            raise Exception()

    async def execute(self, session):
        self.checkSleh()
        await super().execute(session)
        self._response = ImageRequest.parseImageJson(self._response[0])
        return self._response

    @staticmethod
    def parseImageJson(featureJson):
        properties = featureJson['properties']
        geometry = featureJson['geometry']

        geoPoint = model.GeoPoint(geometry['coordinates'][0], geometry['coordinates'][1])
        imageProp = model.ImageProperty(properties['key'], properties['ca'], geoPoint)
        image = model.Image(imageProperty=imageProp, captureDate=parse(properties['captured_at']),
                            cameraMake=properties['camera_make'], cameraModel=properties['camera_model'],
                            sequenceKey=properties['sequence_key'], isPanoram=properties['pano'],
                            userKey=properties['user_key'], username=properties['username'])
        return image


class ImageSearchRequest(ImageObjectSearchRequest):

    def __init__(self, clientId, clientSecret):
        super().__init__(clientId, clientSecret)
        self._requestString += (ImageRequest._imagePrefix + answerPart)

    def addCloseTo(self, geoPoint):
        self.checkAnd()
        self._requestString += ("closeto=" + str(geoPoint))
        return self

    def addLookAt(self, geoPoint):
        self.checkAnd()
        self._requestString += ("lookat=" + str(geoPoint))
        return self

    def addPano(self, isPanoram):
        self.checkAnd()
        self._requestString += ("pano=" + str(isPanoram).lower())
        return self

    def addRadius(self, radius):
        self.checkAnd()
        self._requestString += ("radius=" + str(radius))
        return self

    def addProjectKeys(self, projectKeysList):
        self.checkAnd()
        self._requestString += "project_keys="
        for key in projectKeysList:
            self._requestString += (key + comaPart)
        self._requestString = self._requestString[:-1]
        return self

    def addSequenceKeys(self, sequenceKeysList):
        self.checkAnd()
        self._requestString += "sequence_keys="
        for key in sequenceKeysList:
            self._requestString += (key + comaPart)
        self._requestString = self._requestString[:-1]
        return self

    def parseSearchResponse(self, json):
        images = []
        for feature in json['features']:
            images.append(ImageRequest.parseImageJson(feature))
        return images


class ImageDownloadRequest(APIRequest):
    _cdnPrefix = "https://d1cuyjsrcm0gby.cloudfront.net/"
    _imageResolutions = {320: "/thumb-320.jpg",
                         640: "/thumb-640.jpg",
                         1024: "/thumb-1024.jpg",
                         2048: "/thumb-2048.jpg"}

    def __init__(self, clientId, clientSecret, image, resolution, dirPath):
        super().__init__(clientId, clientSecret)
        self._requestString = ImageDownloadRequest._cdnPrefix
        self._resolution = resolution
        if not os.path.exists(dirPath):
            os.mkdir(dirPath)
        self._dirPath = dirPath
        self._image = image

    async def execute(self, session):
        self._requestString += (self._image.key + ImageDownloadRequest._imageResolutions[self._resolution])
        async with session.get(self._requestString) as response:
            self._response = response.status
            with open(self._dirPath + self._image.getFilename(), "wb") as file:
                file.write(await response.read()) 


class SequenceRequest(APIRequest):
    _sequencePrefix = "sequences"

    def __init__(self, clientId, clientSecret, key):
        super().__init__(clientId, clientSecret)
        self._requestString += (SequenceRequest._sequencePrefix + slehPart + key)

    @staticmethod
    def parseSequenceJson(featureJson):
        properties = featureJson['properties']
        geometry = featureJson['geometry']

        geoPoints = []
        for point in geometry['coordinates']:
            geoPoints.append(model.GeoPoint(point[0], point[1]))
        imageProps = []
        for i in range(len(properties['coordinateProperties']['image_keys'])):
            imageProp = model.ImageProperty(properties['coordinateProperties']['image_keys'][i],
                                            properties['coordinateProperties']['cas'][i], geoPoints[i])
            imageProps.append(imageProp)

        sequence = model.Sequence(key=properties['key'], captureDate=parse(properties['captured_at']),
                                  createdDate=properties['created_at'], imageProperties=imageProps,
                                  userKey=properties['user_key'], username=properties['username'])
        return sequence

    async def execute(self, session):
        await super().execute(session)
        self._response = SequenceRequest.parseSequenceJson(self._response[0])
        return self._response


class SequenceSearchRequest(ImageObjectSearchRequest):

    def __init__(self, clientId, clientSecret):
        super().__init__(clientId, clientSecret)
        self._requestString += (SequenceRequest._sequencePrefix + answerPart)

    def addStarred(self, isStarred):
        self.checkAnd()
        self._requestString += ("starred=" + str(isStarred).lower())
        return self

    def parseSearchResponse(self, json):
        sequences = []
        for feature in json['features']:
            sequences.append(SequenceRequest.parseSequenceJson(feature))
        return sequences


class APIService:
    def __init__(self, credPath):
        with open(credPath, "r") as file:
            self._clientId = file.readline().replace("\n", "")
            self._clientSecret = file.readline().replace("\n", "")

    def createImageRequest(self, key):
        return ImageRequest(self._clientId, self._clientSecret, key)

    def createImageSearchRequest(self):
        return ImageSearchRequest(self._clientId, self._clientSecret)

    def createImageDownloadRequest(self, image, resolution, dirPath):
        return ImageDownloadRequest(self._clientId, self._clientSecret, image, resolution, dirPath)

    def createSequenceRequest(self, key):
        return SequenceRequest(self._clientId, self._clientSecret, key)

    def createSequenceSearchRequest(self):
        return SequenceSearchRequest(self._clientId, self._clientSecret)

    def createCustomRequest(self, requestString):
        request = APIRequest(self._clientId, self._clientSecret)
        request._requestString = request._apiPrefix + requestString
        return request

    def createImagesRequests(self, imageKeys):
        imageRequests = []
        for imageKey in imageKeys:
            imageRequests.append(ImageRequest(self._clientId, self._clientSecret, imageKey))
        return imageRequests

    def createDownloadImagesRequests(self, imagesList, resolution, dirPath):
        downloadRequests = []
        for image in imagesList:
            downloadRequests.append(
                ImageDownloadRequest(self._clientId, self._clientSecret, image, resolution, dirPath))
        return downloadRequests

    def executeRequestsList(self, requestList):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def executer():
            async with aiohttp.ClientSession(loop=loop) as sess:
                for req in requestList:
                    await req.execute(sess)

        loop.run_until_complete(executer())
        loop.close()

    def multithreadingExecuteRequestsList(self, requestsList, threadCount=20):
        def separateRequests(requestsList, count):
            partSize = int(len(requestsList) / count)
            parts = [requestsList[i * partSize: (i + 1) * partSize] for i in range(count)]
            delta = len(requestsList) - partSize * count
            if delta > 0:
                for i in range(delta):
                    parts[count - 1].append(requestsList[len(requestsList) - i - 1])
            return parts

        parts = separateRequests(requestsList, threadCount)
        threads = []
        for i in range(threadCount):
            thread = Thread(target=self.executeRequestsList, args=(parts[i],))
            thread.start()
            threads.append(thread)
        [thread.join() for thread in threads]
