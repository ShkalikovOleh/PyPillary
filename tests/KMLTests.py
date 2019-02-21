import sys
import os.path

currentDir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(currentDir))

import nose
import pypillary.request as request
import pypillary.model as model
import pypillary.utils as utils

class TestKML:
     def test_saveToKML(self):
        service = request.APIService(currentDir + "/clientInfo.txt")
        seq_req = service.createSequenceRequest("_dwKx5EWQ6-TgBt7BXZRaA")
        service.executeRequestsList([seq_req])
        sequence = seq_req.response
        utils.seqToKML(sequence, 2048, currentDir + "/test.kml")