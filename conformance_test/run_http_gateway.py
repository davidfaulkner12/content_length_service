# This module tests that the HTTP Gateway works as described with urllib.request

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import urllib.request
from urllib.error import URLError
from httptools.httpgateway import HttpGateway

if __name__ == '__main__':
    gw = HttpGateway(urllib.request)
    assert(gw.getContentLength('https://www.bbc.com')['contentLength'] > 0)
    assert(gw.getContentLength('https://www.google.com')['contentLength'] > 0)
    try:
        print(gw.getContentLength('bbb://bbb.ccc'))
    except URLError as e:
        pass
    else:
        assert(false)
    assert(gw.getContentLength('https://www.bbc.com/asdf')['statusCode'] == 404)
