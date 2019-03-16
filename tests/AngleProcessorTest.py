import sys
import os.path

currentDir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(currentDir))

import nose
import numpy as np
import pypillary.model as model
import pypillary.processing as processing

class TestAngleProcessor:
    
    def __init__(self):
        imgProps = []
        imgProps.append(model.ImageProperty("Key", 30, model.GeoPoint(30, 40)))
        imgProps.append(model.ImageProperty("Key", 45, model.GeoPoint(31, 39)))
        imgProps.append(model.ImageProperty("Key", 60, model.GeoPoint(29, 41)))
        self.seq = model.Sequence("None", None, None, imgProps, None, None)

    def test_generateCAVectors(self):
        vecs = processing.AngleProcessor.generateCAVectors(self.seq)

        for i in range(len(self.seq.imageProperties)):
            x = np.cos(np.radians(self.seq.imageProperties[i].ca))
            y = np.sin(np.radians(self.seq.imageProperties[i].ca))
            assert(vecs[i][0] == x)
            assert(vecs[i][1] == y)

    def test_generateMovingVector(self):
        vecs = processing.AngleProcessor.generateMovingVectors(self.seq)

        for i in range(len(self.seq.imageProperties) - 1):
            x = self.seq.imageProperties[i+1].geoPoint.longitude - self.seq.imageProperties[i].geoPoint.longitude
            y = self.seq.imageProperties[i+1].geoPoint.latitude - self.seq.imageProperties[i].geoPoint.latitude
            assert(vecs[i][0] == x)
            assert(vecs[i][1] == y)

    def test_angle(self):
        cas = processing.AngleProcessor.generateCAVectors(self.seq)
        movingVecs = processing.AngleProcessor.generateMovingVectors(self.seq)
        angles = processing.AngleProcessor.angle(movingVecs, cas[:len(cas)-1])

        for i in range(len(angles)):            
            dot = cas[i][0] * movingVecs[i][0] + cas[i][1] * movingVecs[i][1]
            normMoving = np.linalg.norm(movingVecs[i])            
            angle = np.arccos(dot / normMoving)
            assert(angle == angles[i])