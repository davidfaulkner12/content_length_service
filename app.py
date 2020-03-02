#!bin/python
# Basic Flask API here -- we accept a POST of a list of URLs and return a list
# with content types and error keys.

from flask import Flask, request, jsonify

from httptools.httpgateway import HttpGateway
from httptools import besthttplib

from urllib.error import URLError

app = Flask(__name__)
# Obviously this is not sophisticated enough for a real application, but
# it allows us to demonstrate testing overrides pretty easily
app.config['HTTP_GW'] = HttpGateway(besthttplib)

@app.route('/content_lengths', methods=['POST'])
def contentLengths():
    """Return a list of content lengths and statuses.

    For each URL in the 'urls' attribute of the request body, return a JSON
    object with the content length (if found), the HTTP status code (if found),
    and an optional errorKey that the front end can use to display a localised
    error message.
    """
    if not request.json or not 'urls' in request.json:
        abort(400)
    urls = request.json['urls']
    results = [_contentLengthForUrl(url) for url in urls]
    return jsonify({"contentLengths": results}), 200

def _contentLengthForUrl(url):
    # We make this logic a little more complicated for demonstration purposes.
    # Our HTTP gateway doesn't throw exceptions for HTTP return codes, but
    # this API returns an error key for both internal errors and remote errors.
    gw = app.config['HTTP_GW']
    try:
        gw_response = gw.getContentLength(url)
        if (gw_response['statusCode'] in _statusCodeToErrorKey):
            gw_response['errorKey'] = (
                _statusCodeToErrorKey[gw_response['statusCode']])
        return gw_response
    except URLError as e:
        return {
            "url": url,
            "errorKey": "urlError"
        }
    except Exception as e:
        return {
            "url": url,
            "errorKey": "unexpectedError"
        }

# Let's not do anything too sophisticated here.
_statusCodeToErrorKey = {
    404: 'notFound',
    418: 'teapot',
    500: 'internalError'
}

if __name__ == '__main__':
    app.run(debug=True)
