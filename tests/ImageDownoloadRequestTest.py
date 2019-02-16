import sys
import os.path
currentDir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(currentDir))

import unittest
import pypillary.request as request
import pypillary.model as model

class ImageDownoloadRequestsTest(unittest.TestCase):
    
    def setUp(self):
        with open(currentDir + "/clientInfo.txt", "r") as file:
            self._clientId = file.readline().replace("\n", "") 
            self._clientSecret = file.readline().replace("\n", "")  


    def testExecuteAsyncTest(self):
        service = request.APIService(currentDir + "/clientInfo.txt")
        img = service.createImageRequest("uTHY8_SvFPOXr16D5oAAUg").get()
        service.executeRequestsListAsync([request.ImageDownloadRequest(self._clientId, self._clientSecret, img ,320, currentDir + "/imgs/")])

if __name__ == '__main__':
    tests = unittest.main(exit=False)
    fcount = len(tests.result.failures)
    ecount = len(tests.result.failures)
    if not fcount == ecount == 0:
        raise ValueError
