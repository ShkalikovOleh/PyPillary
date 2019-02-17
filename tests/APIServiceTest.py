import sys
import os.path

currentDir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(currentDir))

import nose
import pypillary.request as request
import pypillary.model as model


class TestAPIService:

    def setUp(self):
        with open(currentDir + "/clientInfo.txt", "r") as file:
            self.clientId = file.readline().replace("\n", "")
            self.clientSecret = file.readline().replace("\n", "")
        self.service = request.APIService(currentDir + "/clientInfo.txt")

    def test_CreateImageRequest(self):
        req = self.service.createImageRequest("uTHY8_SvFPOXr16D5oAAUg")
        assert isinstance(req, request.ImageRequest)
        assert req.requestString == "https://a.mapillary.com/v3/images/uTHY8_SvFPOXr16D5oAAUg"

    def test_CreateImageSearchRequest(self):
        req = self.service.createImageSearchRequest()
        assert isinstance(req, request.ImageSearchRequest)
        assert req.requestString == "https://a.mapillary.com/v3/images?"

    def test_ExecuteRequestsList(self):        
        requests = [request.ImageRequest(self.clientId, self.clientSecret, "uTHY8_SvFPOXr16D5oAAUg"),
                    request.ImageRequest(self.clientId, self.clientSecret, "uTHY8_SvFPOXr16D5oAAUg")]
        self.service.executeRequestsList(requests)
        for req in requests:
            assert isinstance(req.response, model.Image)

    def test_MultithreadingExecuteRequestsList(self):        
        requests = [request.ImageRequest(self.clientId, self.clientSecret, "uTHY8_SvFPOXr16D5oAAUg") for i in
                    range(100)]
        self.service.multithreadingExecuteRequestsList(requests, 5)
        for req in requests:
            assert isinstance(req.response, model.Image)
            assert req.response.key == "uTHY8_SvFPOXr16D5oAAUg"