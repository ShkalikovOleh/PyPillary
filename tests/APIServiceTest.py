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


    def testExecuteRequestsListAsync(self):
        credPath = currentDir + "/clientInfo.txt"
        service = request.APIService(credPath)
        requests = [request.ImageRequest(self._clientId, self._clientSecret, "uTHY8_SvFPOXr16D5oAAUg"), 
                    request.ImageRequest(self._clientId, self._clientSecret, "uTHY8_SvFPOXr16D5oAAUg")]
        service.executeRequestsListAsync(requests)
        for req in requests:
            self.assertIsInstance(req.response, model.Image)


    def testMultithreadingExecuteRequestsListAsync(self):
        credPath = currentDir + "/clientInfo.txt"
        service = request.APIService(credPath)
        requests = [request.ImageRequest(self._clientId, self._clientSecret, "uTHY8_SvFPOXr16D5oAAUg") for i in range(1000)]
        service.multithreadingExecuteRequestsListAsync(requests,5)
        for req in requests:
            self.assertIsInstance(req.response, model.Image)
            self.assertEqual(req.response.key, "uTHY8_SvFPOXr16D5oAAUg")

if __name__ == '__main__':
    tests = unittest.main(exit=False)
    fcount = len(tests.result.failures)
    ecount = len(tests.result.failures)
    if not fcount == ecount == 0:
        raise ValueError