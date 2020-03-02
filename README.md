# Simple Flask Example with Testing

## tl;dr
This is a toy Flask HTTP API (not really RESTful) that get contentLengths for
a list of URLs, mainly used to demonstrate testing.

## Install and Run
1. Clone the git directory.

```shell
git clone tbd
```

2. (Optional) Create a virtualenv in that directory.

```shell
virtualenv tbd
```

3. Install the requirements
```shell
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
