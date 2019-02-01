import model
import request

service = request.APIService("clientInfo.txt")

geo1 = model.GeoPoint(30.457461388888888,50.448696388888884)
geo2 = model.GeoPoint(30.456461388888888,50.458696388888884)
imgs = service.createImageSearchRequest().addBbox(geo1, geo2). \
        addPano(False).addRadius(225).addPerPage(15).get()
img = service.createImageRequest().key(imgs[0].key).get()
print(img.username)

requests = service.createDownloadImagesRequests(imgs, 320, "imgs/")
service.multithreadingGetRequests(requests, 15)