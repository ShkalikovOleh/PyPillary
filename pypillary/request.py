import pypillary.model as model
import os
import aiohttp
import asyncio
from dateutil.parser import parse
from threading import Thread

andPart = "&"
answerPart = "?"
comaPart = ","
slehPart = "/"


class APIRequest:
    '''
    Базовый класс запроса к сервису Mapillary
    Определяет общие методы по работе с запросами к разным объектам    
    '''
    _apiPrefix = "https://a.mapillary.com/v3/"

    def __init__(self, clientId, clientSecret):        
        self._clientId = clientId
        self._clientSecret = clientSecret
        self._requestString = APIRequest._apiPrefix
        self._response = []

    @property
    def requestString(self):
        '''
        Возвращает текущую строку запроса, по которой пойдет запрос при вызове метода execute(без clientId)
        clientId автоматически добавлятся в методе execute
        '''
        return self._requestString

    @property
    def response(self):
        '''
        После выполнения запроса содержит ответ сервиса в виде list of json
        '''
        return self._response

    def checkAnd(self):
        '''
        В случае необходимости добавляет & к строке requestString для возможности передачи нескольких разных параметров
        '''
        if self._requestString[-1] != '/' and self._requestString[-1] != '&':
            self._requestString += andPart

    async def execute(self, session):
        '''
        Посылает запрос на сервис и получает ответ
        Поддерживает pagination
        
        :param:session объект типа aiohttp.ClientSession, который выполняет запросы

        Возвращает list of json ответа
        '''
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
    '''
    Класс обобщающий создание запросов поиска к последовательностям и изображениям в стиле FluentAPI    
    '''

    def addBbox(self, geoPointMin, geoPointMax):
        '''
        Добавляет к строке запроса параметр поиска в пределах определенного квадрата территории

        :param: geoPointMin - объект типа model.GeoPoint, который указывает на минимальные координаты квадрата поиска
        :param: geoPointMax - объект типа model.GeoPoint, который указывает на максимальныые координаты квадрата поиска
        '''
        self.checkAnd()
        self._requestString += ("bbox=" + str(geoPointMin) + comaPart + str(geoPointMax))
        return self

    def addStartTime(self, datetime):
        '''
        Добавляет к строке запроса параметр поиска, ограничивающий снизу дату его создания

        :param: datetime is datatime type object
        '''
        self.checkAnd()
        self._requestString += ("start_time=" + datetime.isoformat())
        return self

    def addEndTime(self, datetime):
        '''
        Добавляет к строке запроса параметр поиска, ограницивающий сверху дату его создания

        param datetime is datatime type object
        '''
        self.checkAnd()
        self._requestString += ("end_time=" + datetime.isoformat())
        return self

    def addUserkeys(self, userkeysList):
        '''
        Добавляет к строке запроса параметр поиска, позволяющий производить поиск объектов, сделанных конкретными пользователями

        :param: userkeysList список строк, представляющих ключи пользователей
        '''
        self.checkAnd()
        self._requestString += "userkeys="
        for key in userkeysList:
            self._requestString += (key + comaPart)
        self._requestString = self._requestString[:-1]
        return self

    def addUsenames(self, usernamesList):
        '''
        Добавляет к строке запроса параметр поиска, позволяющий производить поиск объектов, сделанных конкретными пользователями

        :param: usernamesList список строк, представляющих имена пользователей
        '''
        self.checkAnd()
        self._requestString += "usernames="
        for name in usernamesList:
            self._requestString += (name + comaPart)
        self._requestString = self._requestString[:-1]
        return self

    def addPerPage(self, countPerPage):
        '''
        Добавляет к строке запроса параметр, который показывает сколько подходящих по параметрам объктам будет передаваться на одной странице ответа
        
        :param: countPerPage - целочисленная переменная. Количество на одной странице ответа. По умолчанию = 200 Максимум = 1000
        '''
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
    '''
    Класс, создающий запросы к конкретным изображениям по их ключу
    Создан для сбора метаданных о изображениях
    '''

    _imagePrefix = "images"

    def __init__(self, clientId, clientSecret, key):
        super().__init__(clientId, clientSecret)
        self._requestString += (self._imagePrefix + slehPart + key)

    async def execute(self, session):       
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
    '''
    Класс для создания запросов по поиску изображений
    '''

    def __init__(self, clientId, clientSecret):
        super().__init__(clientId, clientSecret)
        self._requestString += (ImageRequest._imagePrefix + answerPart)

    def addCloseTo(self, geoPoint):
        '''
        Добавляет параметр поиска изображения вблизи определенной точки
        Используется с addRadius(radius)

        :param: geoPoint - объект типа model.GeoPoint, указывающий точку вблизи которой следует искать
        '''
        self.checkAnd()
        self._requestString += ("closeto=" + str(geoPoint))
        return self

    def addLookAt(self, geoPoint):
        '''
        Добавляет параметр поиска по изображениям, направленных в направлении указанной точки
        Не имеет смысла без использования addCloseTo(geoPoint) или addBbox(geoMin, geoMax)

        :param: geoPoint - объект типа model.GeoPoint, указывающий точку, на которую должны быть направлены изображения из ответа
        '''
        self.checkAnd()
        self._requestString += ("lookat=" + str(geoPoint))
        return self

    def addPano(self, isPanoram):
        '''
        Метод, добавляющий фильтр панорамных изображения

        :param: isPanoram - булева переменная
        '''
        self.checkAnd()
        self._requestString += ("pano=" + str(isPanoram).lower())
        return self

    def addRadius(self, radius):
        '''
        Метод, позволяющий выбрать изображения, которые были сделаны не более чем в определенном радиусе от точки, переданно параметром CloseTo
        Не имеет смысла без применения addCloseTo(geoPoint)

        :param: radius - неотрицательная числовая переменная
        '''
        self.checkAnd()
        self._requestString += ("radius=" + str(radius))
        return self

    def addProjectKeys(self, projectKeysList):
        '''
        Добавляет параметр поиска по изображениям из определенных проектов

        :param: projectKeysList - список строк-ключей проектов
        '''
        self.checkAnd()
        self._requestString += "project_keys="
        for key in projectKeysList:
            self._requestString += (key + comaPart)
        self._requestString = self._requestString[:-1]
        return self

    def addSequenceKeys(self, sequenceKeysList):
        '''
        Добавляет параметр поиска по изображениям из определенных последовательностей

        :param: projectKeysList - список строк-ключей последовательностей
        '''
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
    '''
    Класс для создания запроса на загрузку и непосредственно загрузки изображения
    '''

    _cdnPrefix = "https://d1cuyjsrcm0gby.cloudfront.net/"
    ImageResolutions = {320: "/thumb-320.jpg",
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
        self._requestString += (self._image.key + ImageDownloadRequest.ImageResolutions[self._resolution])
        async with session.get(self._requestString) as response:
            self._response = response.status
            with open(self._dirPath + self._image.getFilename(), "wb") as file:
                file.write(await response.read()) 


class SequenceRequest(APIRequest):
    '''
    Класс, создающий запросы к конкретным последовательностям по их ключу
    Создан для сбора метаданных о последовательностях
    '''

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
    '''
    Класс для создания запросов по поиску последовательностей
    '''

    def __init__(self, clientId, clientSecret):
        super().__init__(clientId, clientSecret)
        self._requestString += (SequenceRequest._sequencePrefix + answerPart)

    def addStarred(self, isStarred):
        '''
        Метод, добавляющий к запросу поиска параметр, который позволит выбирать только 'избранные' последовательности

        :param: isStarred - булевая переменная
        '''        
        if isinstance(isStarred, bool):
            self.checkAnd()
            self._requestString += ("starred=" + str(isStarred).lower())
            return self
        else:
            raise ValueError

    def parseSearchResponse(self, json):
        sequences = []
        for feature in json['features']:
            sequences.append(SequenceRequest.parseSequenceJson(feature))
        return sequences


class APIService:
    '''
    Класс для упрощения работы по созданию и выполнению запросов
    Предпочтительный путь использования данного пакета
    '''
    def __init__(self, credPath):
        with open(credPath, "r") as file:
            self._clientId = file.readline().replace("\n", "")
            self._clientSecret = file.readline().replace("\n", "")

    def createImageRequest(self, key):
        if not isinstance(key, str):
            raise ValueError
        
        return ImageRequest(self._clientId, self._clientSecret, key)        

    def createImageSearchRequest(self):
        return ImageSearchRequest(self._clientId, self._clientSecret)

    def createImageDownloadRequest(self, image, resolution, dirPath):
        '''
        Метод, создающий объет ImageDownloadRequest

        :param: image - объект типа model.Image, изображения которого необходимо загрузить
        :param: resolution - размер изображения (320|640|1024|2048)
        :param: dirPath - путь до папки, в которую будут сохранены файлы изображений
        '''
        if isinstance(image, model.Image) and (resolution in ImageDownloadRequest.ImageResolutions) \
            and isinstance(dirPath, str):
            return ImageDownloadRequest(self._clientId, self._clientSecret, image, resolution, dirPath)
        else:
            raise ValueError

    def createSequenceRequest(self, key):
        if not isinstance(key):
            raise ValueError

        return SequenceRequest(self._clientId, self._clientSecret, key)

    def createSequenceSearchRequest(self):
        return SequenceSearchRequest(self._clientId, self._clientSecret)

    def createCustomRequest(self, requestString):
        if not isinstance(requestString, str):
            raise ValueError
        
        request = APIRequest(self._clientId, self._clientSecret)
        request._requestString += requestString
        return request        

    def executeRequestsList(self, requestList):
        '''
        Метод, выполняющий создание всей необходимой инфраструктры для асинхронного выполнения запросов из списка

        :param: requestList - список запросов для выполнения
        '''
        if not isinstance(requestList, list):
            raise ValueError

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def executer():
            async with aiohttp.ClientSession(loop=loop) as sess:
                for req in requestList:
                    await req.execute(sess)

        loop.run_until_complete(executer())
        loop.close()

    def multithreadingExecuteRequestsList(self, requestList, threadCount=20):
        '''
        Метод, выполняющий запросы в указаном количестве потоков

        :param: requestList - список из объектов request.APIRequest(и производных)
        :param: threadCount - количество потоков(целочисленный беззнаковый параметр - натуральное число)
        '''
        if not (isinstance(requestList, list) or isinstance(threadCount, int)):
            raise ValueError
        
        def separateRequests(requestList, count):
            partSize = int(len(requestList) / count)
            parts = [requestList[i * partSize: (i + 1) * partSize] for i in range(count)]
            delta = len(requestList) - partSize * count
            if delta > 0:
                for i in range(delta):
                    parts[count - 1].append(requestList[len(requestList) - i - 1])
            return parts

        parts = separateRequests(requestList, threadCount)
        threads = []
        for i in range(threadCount):
            thread = Thread(target=self.executeRequestsList, args=(parts[i],))
            thread.start()
            threads.append(thread)
        [thread.join() for thread in threads]