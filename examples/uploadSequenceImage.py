import pypillary.model as model
import pypillary.request as request

import os
currentDir = os.path.dirname(os.path.abspath(__file__))

#Создать сервис, который упрощает выполнение запросов
service = request.APIService(currentDir + "/clientInfo.txt")

#Запросить объект последовательности по заданному ключу(создать запрос и сразу его выполнить)
seq_req = service.createSequenceRequest("_dwKx5EWQ6-TgBt7BXZRaA")
service.executeRequestsListAsync([seq_req])
sequence = seq_req.response 

imgProps = []
if len(sequence.imageProperties) > 1000:
    imgProps = sequence.imageProperties[:1000]
else:
    imgProps = sequence.imageProperties

#Создать запросы по получению объектов изображений, входящих в sequence
imgs_req = [service.createImageRequest(prop.key) for prop in imgProps]
#Выполение запросов асинхронно в 10 потоков
service.multithreadingExecuteRequestsListAsync(imgs_req, 10)

#Получение из поля response запросов объектов изображний
imgs = [req.response for req in imgs_req]

#Создание списка запросов на основе списка изображений
requests = service.createDownloadImagesRequests(imgs, 1024, currentDir + "/imgs/")
#Выполение запросов асинхронно в 25 потоков
service.multithreadingExecuteRequestsListAsync(requests, 25)