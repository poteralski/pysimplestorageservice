# pysimplestorageservice
[![PyPI version](https://badge.fury.io/py/pysimplestorageservice.svg)](https://badge.fury.io/py/pysimplestorageservice)
## Instalation
    pip install pysimplestorageservice

    git clone https://github.com/poteralski/pysimplestorageservice.git
    cd pysimplestorageservice
    python setup.py install
    python setup.py develop

## Example Usage
    from pysimplestorageservice import AmazonAWSManager
    s3 = AmazonAWSManager(access_key='', secret_key='')
    files = s3.get_file_list(
        bucket='my-bucket',
        prefix='media/images/events/',
    )
    dirs = s3.get_dir_list(
        bucket='my-bucket',
        prefix='media/images/',
    )

## References
based on [Authenticating Requests (AWS Signature Version 4)](http://docs.aws.amazon.com/AmazonS3/latest/API/bucket-policy-s3-sigv4-conditions.html)

## Problem
Problem with connect to Signature Version 4 Servers. For example Frankfurt

## Inspiration
boto