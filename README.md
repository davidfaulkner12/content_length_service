# Simple Flask Example with Testing

## tl;dr
This is a toy Flask HTTP API (not really RESTful) that get contentLengths for
a list of URLs, mainly used to demonstrate testing.

Note that this was tested using Python 3.7 and will certainly not work in
Python 2.

## Install and Run
1. Clone the git directory.

```shell
git clone git@github.com:davidfaulkner12/content_length_service.git
```

2. (Optional) Create a virtualenv in that directory.

```shell
virtualenv content_length_service
source content_length_service/bin/activate
```

3. Install the requirements
```shell
cd content_length_service
pip install -r requirements.txt
```

4. Run the tests.
```shell
python -m unittest tests/test_*
```

5. (Optional) Run the conformance tests that url a real urllib
```shell
python conformance_test/run_http_gateway.py
```

6. (Optional) Run the app (with a stub library).
```shell
python app.py
curl -i  -X POST -H "Content-Type: application/json"  -d '{"urls":["https://www.bbc.com/","https://www.google.com/"]}' http://localhost:5000/content_lengths
```
