from urllib.error import HTTPError

# TODO :-)
class Request:
    def __init__(self, url, **kwargs):
        self.url = url
        self.kwargs = kwargs

# TODO :-)
class _Response:
    def __init__(self):
        self.headers = {}
        self.status = 418
        self.body = ''

# TODO :-)
def urlopen(request):
    raise HTTPError(request.url, 418, 'Not implemented yet', {}, None)
