import pypillary.model as model
import pypillary.request as request
from fastkml import kml
from shapely.geometry import Point

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
    placemark = kml.Placemark(name = imageProperty.key, 
        description = '<div><img src=' + '"' + request.ImageDownloadRequest._cdnPrefix + \
                imageProperty.key + request.ImageDownloadRequest.ImageResolutions[320] + \
                '" alt=picture/><p>Camera Angel: ' + str(imageProperty.ca) + '</p></div>')
    placemark.geometry = Point(imageProperty.geoPoint.longitude, imageProperty.geoPoint.latitude)
    kmlDoc.append(placemark)
    return kmlDoc

def seqToKML(sequence, path):
    Kml = kml.KML()
    kmlDoc = kml.Document()
    Kml.append(kmlDoc)
    for imageProperty in sequence.imageProperties:
        kmlDoc = addImagePropertyToKML(imageProperty, kmlDoc)
    xml = kmlDoc.to_string()
    with open(path, 'w') as file:
        file.write(xml)