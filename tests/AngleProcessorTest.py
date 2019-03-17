import sys
import os.path

currentDir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(currentDir))

import nose
import numpy as np
import pypillary.model as model
import pypillary.processing as processing

class TestAngleProcessor:

    def test_generateCAVectors(self):
        cas = [30, 45 , 60]
        cas = np.radians(cas)
        vecs = processing.AngleProcessor.generateCAVectors(cas)

        for i in range(len(cas)):
            x = np.cos(cas[i])
            y = np.sin(cas[i])
            assert(vecs[i][0] == x)
            assert(vecs[i][1] == y)

    def test_generateMovingVector(self):
        geoPoints = [model.GeoPoint(4, 3), model.GeoPoint(2, 3), model.GeoPoint(1, -1)]
        vecs = processing.AngleProcessor.generateMovingVectors(geoPoints)

        for i in range(len(geoPoints) - 1):
            x = geoPoints[i+1].longitude - geoPoints[i].longitude
            y = geoPoints[i+1].latitude - geoPoints[i].latitude
            assert(vecs[i][0] == x)
            assert(vecs[i][1] == y)

    def test_genarateLookingVectors(self):
        cameraGeoPoint = model.GeoPoint(20, 30)
        geoPoints = [model.GeoPoint(4, 3), model.GeoPoint(2, 3), model.GeoPoint(1, -1)]
        vecs = processing.AngleProcessor.generateLookingVectors(geoPoints, cameraGeoPoint)

        for i in range(len(geoPoints)):
            x = geoPoints[i].longitude - cameraGeoPoint.longitude
            y = geoPoints[i].latitude - cameraGeoPoint.latitude
            assert(x == vecs[i][0])
            assert(y == vecs[i][1])

    def test_angle(self):
        cases = [30, 45 , 60]
        geoPoints = [model.GeoPoint(4, 3), model.GeoPoint(2, 3), model.GeoPoint(1, -1)]
        cas = processing.AngleProcessor.generateCAVectors(cases)
        movingVecs = processing.AngleProcessor.generateMovingVectors(geoPoints)
        angles = processing.AngleProcessor.angle(movingVecs, cas[:len(cas)-1])

        for i in range(len(angles)):
            dot = cas[i][0] * movingVecs[i][0] + cas[i][1] * movingVecs[i][1]
            normMoving = np.linalg.norm(movingVecs[i])            
            angle = np.arccos(dot / normMoving)
            assert(angle == angles[i])

    def test_findCameraViewCentoids(self):
        cas = np.radians([30, 45 , 60])
        cameraGeoPoints = [model.GeoPoint(1, 2), model.GeoPoint(-1, -4), model.GeoPoint(3,0)]
        geoPoints = [model.GeoPoint(4, 3), model.GeoPoint(2, 3), model.GeoPoint(1, -1)]
        result = processing.AngleProcessor.findCameraViewCentoids(cas, cameraGeoPoints, geoPoints, 0.86)
        assert(result[0][1] == 1)
        assert(result[1][1] == 2)
        assert(result[2][1] == 0)