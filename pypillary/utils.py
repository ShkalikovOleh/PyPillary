import pypillary.model as model

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
        return [service.createDownloadImageRequest(image, resolution, dirPath) for image in imagesList]
    else:
        raise ValueError
        