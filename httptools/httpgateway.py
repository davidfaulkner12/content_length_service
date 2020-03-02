from urllib.error import HTTPError

# Assuming an amazing 3rd-party library with the same interface as urllib
class HttpGateway:
    """Gateway class to an amazing HTTP library.

    The httpLibrary parameter must implement the same interface as
    urllib.request."""
    def __init__(self, httpLibrary):
        self._httpLibrary = httpLibrary

    def getContentLength(self, url):
        """This function returns the length of data at URL.

        This first makes a HEAD call to URL to get the 'Content-Length', if
        available. If that header is not returned we instead make a GET call and
        return the length of the response body in bytes.

        We capture HTTP error codes and return them; other errors result in
        exceptions.
        """
        try:
            # TODO(upgrade_to_3_8): This is a great candidate for := syntax
            headValue = self._getContentLengthByHead(url)
            if headValue:
                return headValue
            else:
                return self._getContentLengthFromBody(url)
        except HTTPError as e:
            return {"url": url, "statusCode": e.code}


    def _getContentLengthByHead(self, url):
        req = self._httpLibrary.Request(url, method='HEAD')
        with self._httpLibrary.urlopen(req) as response:
            if response.headers['Content-Length']:
                return {
                    "url": url,
                    "contentLength": int(response.headers['Content-Length']),
                    "statusCode": response.status
                }

    def _getContentLengthFromBody(self, url):
        req = self._httpLibrary.Request(url, method='GET')
        with self._httpLibrary.urlopen(req) as response:
            return {"url": url,
                    "contentLength": len(response.read()),
                    "statusCode": response.status}
