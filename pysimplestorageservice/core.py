import urllib2
import hashlib
import hmac
import requests

from pysimplestorageservice.utilities import get_utc_now


class AmazonAWSManager(object):
    """
    """
    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key

    def sign(self, key, msg):
        import hmac
        import hashlib
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

    def get_signature_key(self, key, date_stamp, region_name, service_name):
        k_date = self.sign(('AWS4' + key).encode('utf-8'), date_stamp)
        k_region = self.sign(k_date, region_name)
        k_service = self.sign(k_region, service_name)
        k_signing = self.sign(k_service, 'aws4_request')
        return k_signing

    def put(self, filename, file, prefix, bucket):
        t = get_utc_now()
        method = 'PUT'
        amz_date = t.strftime('%Y%m%dT%H%M%SZ')
        date_stamp = t.strftime('%Y%m%d')
        endpoint = 'https://' + bucket + '.s3.amazonaws.com/' + prefix + '/' + filename
        host = bucket + '.s3.amazonaws.com'
        service = 's3'
        region = 'eu-central-1'

        canonical_uri = '/' + prefix + '/' + filename
        canonical_querystring = ''
        payload_hash = hashlib.sha256(file).hexdigest()
        canonical_headers = 'host:' + host + '\n' + \
                            'x-amz-acl:public-read\n' + \
                            'x-amz-content-sha256:' + payload_hash + '\n' + \
                            'x-amz-date:' + amz_date + '\n'
        signed_headers = 'host;x-amz-acl;x-amz-content-sha256;x-amz-date'
        canonical_request = method + '\n' + \
                            canonical_uri + '\n' + \
                            canonical_querystring + '\n' +  \
                            canonical_headers + '\n' + \
                            signed_headers + '\n' + \
                            payload_hash
        algorithm = 'AWS4-HMAC-SHA256'
        credential_scope = date_stamp + '/' + \
                           region + '/' + \
                           service + '/' + \
                           'aws4_request'
        string_to_sign = algorithm + '\n' + \
                         amz_date + '\n' + \
                         credential_scope + '\n' + \
                         hashlib.sha256(canonical_request).hexdigest()
        signing_key = self.get_signature_key(self.secret_key, date_stamp,
                                           region, service)
        signature = hmac.new(signing_key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()
        authorization_header = algorithm + ' ' + 'Credential=' + self.access_key + '/' + credential_scope + ', ' + \
                               'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature
        headers = {
            'Authorization': authorization_header,
            'Date': t.strftime("%A, %d %B %Y %H:%M:%S"),
            'x-amz-acl': 'public-read',
            'x-amz-content-sha256': payload_hash,
            'x-amz-date': amz_date
            }
        r = requests.put(endpoint, data=file, headers=headers)
        return r.status_code

    def get(self, prefix, filename, bucket):
        t = get_utc_now()
        method = 'GET'
        amz_date = t.strftime('%Y%m%dT%H%M%SZ')
        date_stamp = t.strftime('%Y%m%d')
        host = bucket + '.s3.amazonaws.com'
        endpoint = "http://" + host + "/" + prefix + "/" + filename
        service = 's3'
        region = 'eu-central-1'

        canonical_uri = '/' + prefix + '/' + filename
        canonical_querystring = ''
        payload_hash = hashlib.sha256("").hexdigest()
        canonical_headers = 'host:' + host + '\n' + \
                            'x-amz-acl:public-read\n' + \
                            'x-amz-content-sha256:' + payload_hash + '\n' + \
                            'x-amz-date:' + amz_date + '\n'
        signed_headers = 'host;x-amz-acl;x-amz-content-sha256;x-amz-date'
        canonical_request = method + '\n' + \
                            canonical_uri + '\n' + \
                            canonical_querystring + '\n' +  \
                            canonical_headers + '\n' + \
                            signed_headers + '\n' + \
                            payload_hash
        algorithm = 'AWS4-HMAC-SHA256'
        credential_scope = date_stamp + '/' + \
                           region + '/' + \
                           service + '/' + \
                           'aws4_request'
        string_to_sign = algorithm + '\n' + \
                         amz_date + '\n' + \
                         credential_scope + '\n' + \
                         hashlib.sha256(canonical_request).hexdigest()
        signing_key = self.get_signature_key(self.secret_key, date_stamp,
                                           region, service)
        signature = hmac.new(signing_key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()
        authorization_header = algorithm + ' ' + 'Credential=' + self.access_key + '/' + credential_scope + ', ' + \
                               'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature
        headers = {
            'Authorization': authorization_header,
            'Date': t.strftime("%A, %d %B %Y %H:%M:%S"),
            'x-amz-acl': 'public-read',
            'x-amz-content-sha256': payload_hash,
            'x-amz-date': amz_date
            }
        r = requests.get(endpoint, headers=headers)
        if r.status_code == 200:
            return r.content
        else:
            return r.status_code

    def parse_xml(self, xml_str):
        files = []
        import xml.etree.ElementTree as ET
        import re
        root = ET.fromstring(xml_str)
        # cleaning tags...
        for child in root:
            child.tag = re.sub('{.*}', '', child.tag)
        # listing filenames
        for file in root.findall('Contents'):
            files.append(file[0].text)
        if root.findall('Prefix')[0].text.split("/")[0] == "log_uploads":
            common_prefixes = root.findall('CommonPrefixes')
            if len(common_prefixes) > 0:
                for prefix in common_prefixes[0]:
                    root = self.get_file_list(bucket="stava-applogs",
                                              prefix=prefix.text)
                    return root
        return files

    def parse_xml_for_dirs(self, xml_str):
        files = []
        import xml.etree.ElementTree as ET
        import re
        root = ET.fromstring(xml_str)
        # cleaning tags...
        for child in root:
            child.tag = re.sub('{.*}', '', child.tag)
        # listing filenames
        for file in root.findall('Contents'):
            files.append(file[0].text)
        if root.findall('Prefix')[0].text.split("/")[0] == "log_uploads":
            common_prefixes = root.findall('CommonPrefixes')
            if len(common_prefixes) > 0:
                dirs = []
                for common_prefix in common_prefixes:
                    for prefix in common_prefix:
                        dirs.append(prefix.text.split("/")[-2])
                return dirs
        return files

    def dir_ls(self, list, dir_name):
        filenames = []
        for l in list:
            if dir_name in l:
                filenames.append(l.split("/")[-1])
        return filenames

    def dir_ls_applogs(self, list, dir_name):
        filenames = []
        for l in list:
            if dir_name in l:
                filenames.append(l.split("/")[-2]+"/"+l.split("/")[-1])
        return filenames

    def get_file_list(self, bucket=None, prefix=None, max_keys=None):
        t = get_utc_now()
        method = 'GET'
        amz_date = t.strftime('%Y%m%dT%H%M%SZ')
        date_stamp = t.strftime('%Y%m%d')
        host = bucket + '.s3.amazonaws.com'
        endpoint = "http://" + host
        service = 's3'
        region = 'eu-central-1'

        canonical_uri = '/'
        canonical_querystring = 'delimiter='+urllib2.quote('/',safe='')
        if max_keys is not None:
            canonical_querystring = canonical_querystring + '&max-keys=' + urllib2.quote(str(max_keys),safe='')
        if prefix is not None:
            canonical_querystring = canonical_querystring + '&prefix=' + urllib2.quote(prefix,safe='')
        payload_hash = hashlib.sha256("").hexdigest()
        canonical_headers = 'host:' + host + '\n' + \
                            'x-amz-content-sha256:' + payload_hash + '\n' + \
                            'x-amz-date:' + amz_date + '\n'
        signed_headers = 'host;x-amz-content-sha256;x-amz-date'
        canonical_request = method + '\n' + \
                            canonical_uri + '\n' + \
                            canonical_querystring + '\n' +  \
                            canonical_headers + '\n' + \
                            signed_headers + '\n' + \
                            payload_hash
        #print canonical_request
        algorithm = 'AWS4-HMAC-SHA256'
        credential_scope = date_stamp + '/' + \
                           region + '/' + \
                           service + '/' + \
                           'aws4_request'
        string_to_sign = algorithm + '\n' + \
                         amz_date + '\n' + \
                         credential_scope + '\n' + \
                         hashlib.sha256(canonical_request).hexdigest()
        signing_key = self.get_signature_key(self.secret_key, date_stamp,
                                           region, service)
        signature = hmac.new(signing_key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()
        authorization_header = algorithm + ' ' + 'Credential=' + self.access_key + '/' + credential_scope + ',' + \
                               'SignedHeaders=' + signed_headers + ',' + 'Signature=' + signature
        #print authorization_header

        headers = {
            'Authorization': authorization_header,
            'Date': t.strftime("%A, %d %B %Y %H:%M:%S"),
            'x-amz-content-sha256': payload_hash,
            'x-amz-date': amz_date
            }
        r = requests.get(endpoint+"/?"+canonical_querystring, headers=headers)
        if r.status_code == 200:
            return self.parse_xml(r.content)
        else:
            return None

    def get_dir_list(self, bucket=None, prefix=None, max_keys=None):
        t = get_utc_now()
        method = 'GET'
        amz_date = t.strftime('%Y%m%dT%H%M%SZ')
        date_stamp = t.strftime('%Y%m%d')
        host = bucket + '.s3.amazonaws.com'
        endpoint = "http://" + host
        service = 's3'
        region = 'eu-central-1'

        canonical_uri = '/'
        canonical_querystring = 'delimiter='+urllib2.quote('/',safe='')
        if max_keys is not None:
            canonical_querystring = canonical_querystring + '&max-keys=' + urllib2.quote(str(max_keys),safe='')
        if prefix is not None:
            canonical_querystring = canonical_querystring + '&prefix=' + urllib2.quote(prefix,safe='')
        payload_hash = hashlib.sha256("").hexdigest()
        canonical_headers = 'host:' + host + '\n' + \
                            'x-amz-content-sha256:' + payload_hash + '\n' + \
                            'x-amz-date:' + amz_date + '\n'
        signed_headers = 'host;x-amz-content-sha256;x-amz-date'
        canonical_request = method + '\n' + \
                            canonical_uri + '\n' + \
                            canonical_querystring + '\n' +  \
                            canonical_headers + '\n' + \
                            signed_headers + '\n' + \
                            payload_hash
        #print canonical_request
        algorithm = 'AWS4-HMAC-SHA256'
        credential_scope = date_stamp + '/' + \
                           region + '/' + \
                           service + '/' + \
                           'aws4_request'
        string_to_sign = algorithm + '\n' + \
                         amz_date + '\n' + \
                         credential_scope + '\n' + \
                         hashlib.sha256(canonical_request).hexdigest()
        signing_key = self.get_signature_key(self.secret_key, date_stamp,
                                           region, service)
        signature = hmac.new(signing_key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()
        authorization_header = algorithm + ' ' + 'Credential=' + self.access_key + '/' + credential_scope + ',' + \
                               'SignedHeaders=' + signed_headers + ',' + 'Signature=' + signature
        #print authorization_header

        headers = {
            'Authorization': authorization_header,
            'Date': t.strftime("%A, %d %B %Y %H:%M:%S"),
            'x-amz-content-sha256': payload_hash,
            'x-amz-date': amz_date
            }
        r = requests.get(endpoint+"/?"+canonical_querystring, headers=headers)
        if r.status_code == 200:
            return self.parse_xml_for_dirs(r.content)
        else:
            return None
