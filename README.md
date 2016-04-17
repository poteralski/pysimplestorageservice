# pysimplestorageservice
[![PyPI version](https://badge.fury.io/py/pysimplestorageservice.svg)](https://badge.fury.io/py/pysimplestorageservice)
## Instalation
```bash
    pip install pysimplestorageservice

    git clone https://github.com/poteralski/pysimplestorageservice.git
    cd pysimplestorageservice
    python setup.py install
    python setup.py develop
```
## Example Usage
### `AmazonAWSManager`
#### `get`
```python
from pysimplestorageservice import AmazonAWSManager
amazon = AmazonAWSManager(
    access_key=AWS_ACCESS_KEY_ID,
    secret_key=AWS_SECRET_ACCESS_KEY
)
result = amazon.get(
    bucket=TEST_BUCKET,
    prefix=TEST_DIR,
    filename=TEST_FILE,
)
output = open(TEST_FILE, "wb")
output.write(result)
output.close()
```
#### `get_file_list`
```python
from pysimplestorageservice import AmazonAWSManager
amazon = AmazonAWSManager(
    access_key=AWS_ACCESS_KEY_ID,
    secret_key=AWS_SECRET_ACCESS_KEY
)
files = amazon.get_file_list(
    bucket=TEST_BUCKET,
    prefix=TEST_DIR+'/',
)
print files
```
#### `put`
```python
from pysimplestorageservice import AmazonAWSManager
amazon = AmazonAWSManager(
    access_key=AWS_ACCESS_KEY_ID,
    secret_key=AWS_SECRET_ACCESS_KEY
)
filaname = 'test2.jpg'
file1 = open(filaname, 'r').read()
respond = amazon.put(filename=filaname, file=file1, prefix='test', bucket=TEST_BUCKET)
```
### `AuthSigV4`
You can use this class for authenticate you own requests, for example:
#### `get_headers`
Argument | Type | Description
-------- | ---- | -----------
`bucket` | `str` | Amazon S3 Bucket Name
`method` | `str` | Amazon S3 Method
`canonical_uri='/'` | `str` | Path to file/files
`payload=''` | `str` | Payloads to sign
`querystring={}` | `Dict` | HTTP QueryString to sign
```python
from pysimplestorageservice.auth import AuthSigV4

auth = AuthSigV4(access_key='access_key', secret_key='secret_key')
headers = auth.get_headers('bucket-name', 'GET', canonical_uri='path/to/file.jpg'
file_url = self.__build_endpoint(bucket, prefix, filename)
r = requests.get(file_url, headers=headers)
```
## References
based on [Authenticating Requests (AWS Signature Version 4)](http://docs.aws.amazon.com/AmazonS3/latest/API/bucket-policy-s3-sigv4-conditions.html)

## Problem
Problem with connect to Servers with Signature Version 4 Auth like Frankfurt

### License
This package is available under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).
