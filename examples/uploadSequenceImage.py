import pypillary.model as model
import pypillary.request as request
import pypillary.utils as utils

import os
currentDir = os.path.dirname(os.path.abspath(__file__))

#Создать сервис, который упрощает выполнение запросов
service = request.APIService(currentDir + "/clientInfo.txt")

#Запросить объект последовательности по заданному ключу(создать запрос и сразу его выполнить)
seq_req = service.createSequenceRequest("zBf7pKqFS0ynf51GU3ReMg")
service.executeRequestsList([seq_req])
sequence = seq_req.response 
imgsKey = [im.key for im in seq_req.response.imageProperties]
#Создание списка запросов на основе списка изображений
requests = utils.createDownloadImageRequestList(service, imgsKey, 1024, currentDir + "/imgs/")
#Выполение запросов асинхронно в 25 потоков
service.multithreadingExecuteRequestsList(requests, 25)