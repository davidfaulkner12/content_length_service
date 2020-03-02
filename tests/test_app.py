import unittest
from unittest import TestCase, mock

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

# TODO There are a lot of repeated strings and numbers here that
# could be abstracted away -- this is an excellent candidate for a
# data-driven test.
class AppTest(TestCase):

    def setUp(self):
        # We let the individual tests manage their own expected results.
        self.testGateway = mock.MagicMock()
        app.config['HTTP_GW'] = self.testGateway

    def test_happySingleUrl(self):
        self.testGateway.getContentLength.return_value = {
            'url': 'https://www.bbc.com/',
            'statusCode': 200,
            'contentLength': 42
        }
        with app.test_client() as c:
            rv = c.post('/content_lengths', json={
                "urls": [
                    'https://www.bbc.com/'
                ]
            }).get_json()
            self.assertTrue(
                rv['contentLengths'][0]['url'], 'https://www.bbc.com/')
            self.assertTrue(rv['contentLengths'][0]['statusCode'], 200)
            self.assertTrue(rv['contentLengths'][0]['contentLength'], 42)

    def test_notFoundSingleUrl(self):
        self.testGateway.getContentLength.return_value = {
            'url': 'https://www.bbc.com/',
            'statusCode': 404,
        }
        with app.test_client() as c:
            rv = c.post('/content_lengths', json={
                "urls": [
                    'https://www.bbc.com/'
                ]
            }).get_json()
            self.assertTrue(
                rv['contentLengths'][0]['url'], 'https://www.bbc.com/')
            self.assertTrue(rv['contentLengths'][0]['statusCode'], 404)
            self.assertTrue(rv['contentLengths'][0]['errorKey'], 'notFound')

    def test_happyMultipleUrls(self):
        self.testGateway.getContentLength.side_effect = [{
            'url': 'https://www.bbc.com/',
            'statusCode': 200,
            'contentLength': 42
        }, {
            'url': 'https://www.google.com/',
            'statusCode': 200,
            'contentLength': 2020
        }]
        with app.test_client() as c:
            rv = c.post('/content_lengths', json={
                "urls": [
                    'https://www.bbc.com/',
                    'https://www.google.com'
                ]
            }).get_json()
            self.assertTrue(
                rv['contentLengths'][0]['url'], 'https://www.bbc.com/')
            self.assertTrue(rv['contentLengths'][0]['statusCode'], 200)
            self.assertTrue(rv['contentLengths'][0]['contentLength'], 42)
            self.assertTrue(
                rv['contentLengths'][1]['url'], 'https://www.google.com/')
            self.assertTrue(rv['contentLengths'][1]['statusCode'], 200)
            self.assertTrue(rv['contentLengths'][1]['contentLength'], 2020)
