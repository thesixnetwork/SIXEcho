# Example
```
from sixecho import Client
client = Client()
....
```

# Test 
## Configure
To configure the nosetests command, add a [nosetests] section to your setup.cfg file.

## Run all cases
```
python setup.py nosetests
```
## Run test single test case
```
python setup.py nosetests --tests sixecho/tests/test_client.py:TestSixecho.test_tokenize
```

# Upload pypi 
```
python -m twine upload --repository testpypi dist/*
```