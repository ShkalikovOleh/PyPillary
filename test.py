import model
import request

service = request.APIService("clientInfo.txt")

geo1 = model.GeoPoint(30.457461388888888,50.448696388888884)
geo2 = model.GeoPoint(30.456461388888888,50.458696388888884)
imgsReq = service.createImageSearchRequest().addCloseTo(geo2). \
        addPano(False).addRadius(200).addPerPage(200)
imgs = imgsReq.get()
img = service.createImageRequest(imgs[0].key).get()
seq = service.createSequenceRequest(img.sequenceKey).get()

print(seq.createdDate)

seqs = service.createSequenceSearchRequest().addBbox(geo1, geo2).get()
print(len(seqs))
#requests = service.createDownloadImagesRequests(imgs[100:200], 320, "imgs/")
#service.multithreadingGetRequests(requests, 10)