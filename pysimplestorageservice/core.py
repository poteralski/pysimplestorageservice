import requests

from pysimplestorageservice.auth import AuthSigV4


class AmazonAWSManager(object):
    """
    """
    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key

    def get(self, prefix, filename, bucket):
        """
        GET
        """
        auth = AuthSigV4(access_key=self.access_key, secret_key=self.secret_key)
        headers = auth.get_headers(bucket, 'GET', canonical_uri=self.build_cannonical_uri(filename, prefix))
        file_url = self.__build_endpoint(bucket, prefix, filename)
        r = requests.get(file_url, headers=headers)
        if r.status_code == 200:
            return r.content
        else:
            return r.status_code

    def get_file_list(self, bucket=None, prefix=None, max_keys=None):
        """
        FILE LIST
        """
        params = {"delimiter": "/"}
        if max_keys:
            params["max-keys"] = str(max_keys)
        if prefix:
            params["prefix"] = prefix
        auth = AuthSigV4(access_key=self.access_key, secret_key=self.secret_key)
        headers = auth.get_headers(bucket, 'GET', querystring=params)
        endpoint = self.__build_endpoint(bucket)
        r = requests.get(endpoint, headers=headers, params=params)
        if r.status_code == 200:
            return r.content
        else:
            return None

    def put(self, filename, file, prefix, bucket):
        auth = AuthSigV4(access_key=self.access_key, secret_key=self.secret_key)
        headers = auth.get_headers(bucket, 'PUT', payload=file, canonical_uri=self.build_cannonical_uri(filename, prefix))
        endpoint = self.__build_endpoint(bucket, prefix, filename)
        r = requests.put(endpoint, data=file, headers=headers)
        return r

    def build_cannonical_uri(self, filename, prefix):
        return '/' + prefix + '/' + filename

    def __build_endpoint(self, bucket, prefix=None, filename=None):
        endpoint = "http://" + bucket + '.s3.amazonaws.com'
        if prefix and filename:
            return "/".join([endpoint, prefix, filename])
        elif prefix:
            return "/".join([endpoint, prefix])
        else:
            return endpoint