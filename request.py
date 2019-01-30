import model
import requests

apiPrefix = "https://a.mapillary.com/v3/"
cdnPrefix = "https://d1cuyjsrcm0gby.cloudfront.net/"
clientId = ""
clientSecret = ""
imagePrefix = "images/"
sequencePrefix = "sequences/"
andPart = "&"
answerPart = "?"
imageResolutions = {320: "/thumb-320.jpg",
                    640: "/thumb-640.jpg",
                    1024: "/thumb-1024.jpg",
                    2048: "/thumb-320.jpg}"}


def loadClientInfo(path):
    global clientId
    global clientSecret
    with open(path, "r") as file:
        clientId = file.readline()
        clientSecret = file.readline()


def downoloadImage(image, resolution, directoryPath):    
    response = requests.get(cdnPrefix + image.key + imageResolutions[resolution])
    with open(directoryPath + image.getFilename, "wb") as file:
        file.write(response.content)