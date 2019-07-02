# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.emotion_timeline import EmotionTimeline  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.test import BaseTestCase


class TestEmotionController(BaseTestCase):
    """EmotionController integration test stubs"""

    @unittest.skip("video/webm not supported by Connexion")
    def test_predict_video(self):
        """Test case for predict_video

        predicts the emotions in from still images in a video over time
        """
        body = (BytesIO(b'some file data'), 'file.txt')
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'video/webm',
        }
        response = self.client.open(
            '/api/v1/predict/video',
            method='POST',
            headers=headers,
            data=json.dumps(body),
            content_type='video/webm')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
