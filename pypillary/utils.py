import pypillary.model as model
import simplekml
import pypillary.request as request

def createImageRequestList(service, imageKeys):
    if isinstance(imageKeys, list):
        return [service.createImageRequest(imageKey) for imageKey in imageKeys]        
    else:
        raise ValueError

def createImageFromKey(key):
    if isinstance(key, str):
        imgProp = model.ImageProperty(key, None, None)
        return model.Image(imgProp, None, None, None, None, None, None, None)

def createDownloadImageRequestList(service, imagesList, resolution, dirPath):
    if isinstance(imagesList, list):
        if len(imagesList) > 0:
            if isinstance(imagesList[0], str):
                imagesList = [createImageFromKey(key) for key in imagesList]                    
        return [service.createImageDownloadRequest(image, resolution, dirPath) for image in imagesList]
    else:
        raise ValueError

def addImagePropertyToKML(imageProperty, kmlDoc):    
    point = kmlDoc.newpoint()    
    point.coords = [(imageProperty.geoPoint.longitude, imageProperty.geoPoint.latitude)]
    point.name = imageProperty.key
    point.description = '<div><img src=' + '"' + request.ImageDownloadRequest._cdnPrefix + \
                imageProperty.key + request.ImageDownloadRequest.ImageResolutions[320] + \
                '" alt=picture/><p>Camera Angel: ' + str(imageProperty.ca) + '</p></div>'
    return kmlDoc

def seqToKML(sequence, path):
    kml = simplekml.Kml()    
    for imageProperty in sequence.imageProperties:
        kml = addImagePropertyToKML(imageProperty, kml)
    kml.save(path)