import numpy as np

class AngleProcessor:
    
    @staticmethod
    def generateCAVectors(sequence):
        angles = np.radians(np.array([prop.ca for prop in sequence.imageProperties]))
        X = np.cos(angles)
        Y = np.sin(angles)
        return np.column_stack((X,Y))

    @staticmethod
    def generateMovingVectors(sequence):
        points = np.array([[prop.geoPoint.longitude, prop.geoPoint.latitude] for prop in sequence.imageProperties])
        vecs = np.diff(points, axis=0)
        return vecs

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