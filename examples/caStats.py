import sys
import os.path

currentDir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(currentDir))

import math
import numpy as np
import pypillary.model as model
import pypillary.request as request
import pypillary.utils as utils

service = request.APIService(currentDir + "/clientInfo.txt")
keys = ["_dwKx5EWQ6-TgBt7BXZRaA", "kCqJOH1tnX21LzO310jhPg", ""]
reqs = [service.createSequenceRequest(key) for key in keys]
service.executeRequestsList(reqs)

def dot(v1, v2):
    return (v1[0] * v2[0] + v1[1] * v2[1])

def size(v1):
    x= v1[0]**2
    y = v1[1]**2
    return math.sqrt(x + y)

def angle(v1, v2):
    s1 = size(v1)
    s2 = size(v2)
    prod = dot(v1, v2)
    cos = prod / s1 / s2
    return math.degrees(math.acos(cos))

for i in range(len(reqs)):
    response = reqs[i].response    
    coords = []
    cameraVecs = []
    for j in range(1, len(response.imageProperties)):       
        x = response.imageProperties[j].geoPoint.longitude - response.imageProperties[j-1].geoPoint.longitude
        y = response.imageProperties[j].geoPoint.latitude - response.imageProperties[j-1].geoPoint.latitude
        ca = response.imageProperties[i-1].ca
        cameraVecs.append((math.cos(math.radians(ca)), math.sin(math.radians(ca))))
        coords.append((x,y))
    utils.seqToKML(response, currentDir + "/Seq" + str(i) + ".kml")
    horizontal = (1, 0)
    vertical = (0, 1)    

    angles = [angle(cameraVecs[i], coords[i]) for i in range(len(coords))]
    with open(currentDir + "/Andels" + i + "txt", "w") as file:
        for angle in angles:
            file.write(angle)
    med = np.median(prods)
    var = np.var(prods)
    print(med)
    print(var)