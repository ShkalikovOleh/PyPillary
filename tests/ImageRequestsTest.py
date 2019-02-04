import unittest
import pypillary.model
import pypillary.request as request

class ImageRequestsTest(unittest.TestCase):    

    def setUp(self):
        with open("clientInfo.txt", "r") as file:
            self._clientId = file.readline().replace("\n", "") 
            self._clientSecret = file.readline().replace("\n", "")        


    def testGetImage(self):
        img = request.ImageRequest(self._clientId, self._clientSecret, "uTHY8_SvFPOXr16D5oAAUg").get()
        self.assertIsNotNone(img)        
        self.assertIsInstance(img, pypillary.model.Image)    

if __name__ == '__main__':
    unittest.main()