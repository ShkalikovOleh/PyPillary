import sys
import os.path
currentDir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(currentDir))

import unittest
import pypillary.request as request
import pypillary.model as model

class ImageRequestsTest(unittest.TestCase):    

    def setUp(self):
        with open(currentDir + "/clientInfo.txt", "r") as file:
            self._clientId = file.readline().replace("\n", "") 
            self._clientSecret = file.readline().replace("\n", "")        


    def testGetImage(self):
        img = request.ImageRequest(self._clientId, self._clientSecret, "uTHY8_SvFPOXr16D5oAAUg").get()               
        self.assertIsInstance(img, model.Image)
        self.assertTrue(img.key == "uTHY8_SvFPOXr16D5oAAUg")
        self.assertIsNotNone(img.captureDate)

if __name__ == '__main__':
    unittest.main(exit=False)