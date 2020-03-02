import unittest
from unittest import TestCase, mock

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from httptools.httpgateway import HttpGateway
from urllib.error import HTTPError, URLError

class HttpGatewayTest(TestCase):

    def setUp(self):
        self.mockHttplib = mock.MagicMock()
        self.mockResponse = mock.MagicMock(name="response")

        # This may require a bit of explanation -- techncially the immediately
        # following line is optional and we could implement this with just
        # self.mockHttpLib.urlopen.return_value.__enter__.return_value = (
        #     self.mockResponse)
        # BUT that depends entirely on knowing that we only call urlopen in a
        # with block, which I consider an implementation detail that shouldn't
        # be tested.
        self.mockHttplib.urlopen.return_value = self.mockResponse
        self.mockResponse.__enter__.return_value = self.mockResponse

        self.gw = HttpGateway(self.mockHttplib)

    def test_headResponse(self):
        self.mockResponse.headers = {'Content-Length': 15}
        self.mockResponse.status = 200

        validUrl = 'https://my.valid.url'
        result = self.gw.getContentLength(validUrl)

        self.assertEqual(result['url'], validUrl)
        self.assertEqual(result['contentLength'], 15)
        self.assertEqual(result['statusCode'], 200)
        self.mockResponse.read.assert_not_called()

    def test_bodyResponse(self):
        bodyText = 'I\'m a little teapot, short and stout'
        self.mockResponse.headers.__getitem__.return_value = None
        self.mockResponse.status = 200
        self.mockResponse.read.return_value = bodyText

        validUrl = 'https://my.valid.url'
        result = self.gw.getContentLength(validUrl)

        self.assertEqual(result['url'], validUrl)
        self.assertEqual(result['contentLength'], len(bodyText))
        self.assertEqual(result['statusCode'], 200)

    def test_notFound(self):
        noContentUrl = 'https://my.valid.url/no_content_here',

        self.mockHttplib.urlopen.side_effect = (
            HTTPError(noContentUrl,
                      404, 'Nothing to see here', {}, None))


        result = self.gw.getContentLength(noContentUrl)

        self.assertEqual(result['url'], noContentUrl)
        self.assertEqual(result['statusCode'], 404)

    def test_badUrl(self):
        self.mockHttplib.urlopen.side_effect = URLError("Invalid URL")

        with self.assertRaises(URLError):
            self.gw.getContentLength("aaa://invalid.url")

if __name__ == '__main__':
    unittest.main()
