# pysimplestorageservice
[![PyPI version](https://badge.fury.io/py/pysimplestorageservice.svg)](https://badge.fury.io/py/pysimplestorageservice)
## Instalation
    pip install pysimplestorageservice

    git clone https://github.com/poteralski/pysimplestorageservice.git
    cd pysimplestorageservice
    python setup.py install
    python setup.py develop

## Example Usage
### `AmazonAWSManager`
#### `get`
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
#### `get_file_list`
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
#### `put`
    from pysimplestorageservice import AmazonAWSManager
    amazon = AmazonAWSManager(
        access_key=AWS_ACCESS_KEY_ID,
        secret_key=AWS_SECRET_ACCESS_KEY
    )
    filaname = 'test2.jpg'
    file1 = open(filaname, 'r').read()
    respond = amazon.put(filename=filaname, file=file1, prefix='test', bucket=TEST_BUCKET)
### `AuthSigV4`
You can use this class for authenticate you own requests, for example:

    from pysimplestorageservice.auth import AuthSigV4
    auth = AuthSigV4(access_key='access_key', secret_key='secret_key')
    headers = auth.get_headers(bucket, 'GET', canonical_uri=self.build_cannonical_uri(filename, prefix))
    file_url = self.__build_endpoint(bucket, prefix, filename)
    r = requests.get(file_url, headers=headers)

## References
based on [Authenticating Requests (AWS Signature Version 4)](http://docs.aws.amazon.com/AmazonS3/latest/API/bucket-policy-s3-sigv4-conditions.html)

## Problem
Problem with connect to Servers with Signature Version 4 Auth like Frankfurt
