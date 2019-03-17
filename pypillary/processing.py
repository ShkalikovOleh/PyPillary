import numpy as np

class AngleProcessor:
    
    @staticmethod
    def generateCAVectors(cas):
        '''
        ::param:: cas - list of camera angles in radians
        '''
        angles = np.array([ca for ca in cas])
        X = np.cos(angles)
        Y = np.sin(angles)
        return np.column_stack((X,Y))

    @staticmethod
    def generateMovingVectors(geoPoints):
        points = np.array([[point.longitude, point.latitude] for point in geoPoints])
        vecs = np.diff(points, axis=0)
        return vecs

    @staticmethod
    def generateLookingVectors(geoPoints, cameraGeoPoint):
        points = np.array([[point.longitude, point.latitude] for point in geoPoints])
        cameraPoint = np.array([cameraGeoPoint.longitude, cameraGeoPoint.latitude])
        lookingVecs = np.subtract(points, cameraPoint)
        return lookingVecs

    @staticmethod
    def angle(vecs1, vecs2):
        '''
        Calculate array of angles in rad between vectors in np arrays
        '''
        normVecs1 = np.linalg.norm(vecs1, axis=1)
        normVecs2 = np.linalg.norm(vecs2, axis=1)
        normProd = normVecs1 * normVecs2
        dots = np.sum(vecs1 * vecs2, axis=1)
        return np.arccos(dots/normProd)

    @staticmethod
    def findCameraViewCentoids(cas, cameraGeoPoints, centoidGeoPoints, cameraViewAngel):
        '''
        ::param:: cas - list of camera angles in radians
        ::param:: cameraViewAngle - angel of view of camera in radians
        '''
        caVecs = AngleProcessor.generateCAVectors(cas)        
        cameraViewCentroids = []
        for i in range(len(caVecs)):
            lookingVecs = AngleProcessor.generateLookingVectors(centoidGeoPoints, cameraGeoPoints[i])
            caVec = np.ones((len(lookingVecs), 2)) * caVecs[i]
            angles = AngleProcessor.angle(caVec, lookingVecs)
            candidatIndx = np.argwhere(cameraViewAngel > angles)
            candidates = []
            for j in candidatIndx:
                candidates.append(lookingVecs[j[0]])
            norms = np.linalg.norm(candidates, axis = 1)
            index = np.argmin(norms)
            cameraViewCentroids.append((centoidGeoPoints[index], index))
    
        return cameraViewCentroids