import sys
import os.path
currentDir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(currentDir))

import unittest
import pypillary.request as request
import pypillary.model as model

class APIServiceTest(unittest.TestCase):    

    def setUp(self):
        with open(currentDir + "/clientInfo.txt", "r") as file:
            self._clientId = file.readline().replace("\n", "") 
            self._clientSecret = file.readline().replace("\n", "")            

    def testExecuteAsync(self):
        credPath = currentDir + "/clientInfo.txt"
        service = request.APIService(credPath)
        requests = [request.ImageRequest(self._clientId, self._clientSecret, "uTHY8_SvFPOXr16D5oAAUg"), 
                    request.ImageRequest(self._clientId, self._clientSecret, "uTHY8_SvFPOXr16D5oAAUg")]
        res = service.executeAsync(requests)        
        self.assertIsInstance(res[0], model.Image)


if __name__ == '__main__':
    unittest.main(exit=False)