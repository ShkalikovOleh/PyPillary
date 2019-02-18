import sys
import os.path

currentDir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(currentDir))

import nose
import pypillary.request as request
import pypillary.model as model
import pypillary.utils as utils


class TestAPIService:

    def __init__(self):
        with open(currentDir + "/clientInfo.txt", "r") as file:
            self.clientId = file.readline().replace("\n", "")
            self.clientSecret = file.readline().replace("\n", "")
        self.service = request.APIService(currentDir + "/clientInfo.txt")

    def test_CreateImageRequestCorrectData(self):
        req = self.service.createImageRequest("uTHY8_SvFPOXr16D5oAAUg")
        assert isinstance(req, request.ImageRequest)
        assert req.requestString == "https://a.mapillary.com/v3/images/uTHY8_SvFPOXr16D5oAAUg"

    def test_CreateImageRequestIncorrectData(self):     
        nose.tools.assert_raises(ValueError, self.service.createImageRequest, 14568)

    def test_CreateImageSearchRequest(self):
        req = self.service.createImageSearchRequest()
        assert isinstance(req, request.ImageSearchRequest)        

    def test_CreateImageDownloadRequestCorrectData(self):
        img = utils.createImageFromKey("uTHY8_SvFPOXr16D5oAAUg")
        req = self.service.createImageDownloadRequest(img, 2048, "imgs/")
        assert isinstance(req, request.ImageDownloadRequest)
        assert req.requestString == ("https://d1cuyjsrcm0gby.cloudfront.net/" + "uTHY8_SvFPOXr16D5oAAUg" + "/thumb-2048.jpg")

    def test_CreateImageDownoloadRequestIncorrectImage(self):
        nose.tools.assert_raises(ValueError, self.service.createImageDownloadRequest, 
                                "incorrect", 2048, "imgs/")

    def test_CreateImageDownloadRequestIncorrectResolution(self):
        img = utils.createImageFromKey("uTHY8_SvFPOXr16D5oAAUg")
        nose.tools.assert_raises(ValueError, self.service.createImageDownloadRequest, img, 1080, "imgs/")

    def test_CreateImageDownloadRequestIncorrectDirPath(self):
        img = utils.createImageFromKey("uTHY8_SvFPOXr16D5oAAUg")
        nose.tools.assert_raises(ValueError, self.service.createImageDownloadRequest, img, 1080, 94)

    def test_CreateSequenceRequestCorrectKey(self):
        req = self.service.createSequenceRequest("_dwKx5EWQ6-TgBt7BXZRaA")
        assert isinstance(req, request.SequenceRequest)
        assert req.requestString == "https://a.mapillary.com/v3/sequences/_dwKx5EWQ6-TgBt7BXZRaA"

    def test_CreateSequenceRequestIncorrectKey(self):
        nose.tools.assert_raises(ValueError, self.service.createSequenceRequest, 950486)

    def test_CreateSequenceSearchRequest(self):
        req = self.service.createSequenceSearchRequest()
        assert isinstance(req, request.SequenceSearchRequest)

    def createCustomRequestCorrectData(self):
        string = "something"
        req = self.service.createCustomRequest(string)
        assert isinstance(req, request.APIRequest)
        assert req.requestString == ("https://a.mapillary.com/v3/" + string)

    def createCustomRequestIncorrectData(self):
        nose.tools.assert_raises(ValueError, self.service.createCustomRequest, 15486)

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