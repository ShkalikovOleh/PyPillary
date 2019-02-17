import sys
import os.path
currentDir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(currentDir))

import aiohttp
import asyncio
import pypillary.request as request
import pypillary.model as model

class TestImageRequests:    

    def setUp(self):
        with open(currentDir + "/clientInfo.txt", "r") as file:
            self._clientId = file.readline().replace("\n", "") 
            self._clientSecret = file.readline().replace("\n", "")     

    def executeAsync(self, req):
        async def execute(req):
            async with aiohttp.ClientSession() as sess:
                await req.execute(sess)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(execute(req))

    def test_GetImage(self):
        img_req = request.ImageRequest(self._clientId, self._clientSecret, "uTHY8_SvFPOXr16D5oAAUg")        
        self.executeAsync(img_req)
        img = img_req.response
        assert isinstance(img, model.Image)
        assert img.key == "uTHY8_SvFPOXr16D5oAAUg"
        assert img.captureDate is not None