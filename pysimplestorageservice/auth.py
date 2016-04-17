import hashlib
import hmac
import urllib

from .utilities import get_utc_now


class AuthSigV4(object):
    def __init__(self, access_key, secret_key, algorithm='AWS4-HMAC-SHA256', region='eu-central-1'):
        self.access_key = access_key
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.region = region
        self.service = 's3'
        self.signed_headers = ';'.join(['host', 'x-amz-acl', 'x-amz-content-sha256', 'x-amz-date'])
        self.t = get_utc_now()

    @property
    def date_stamp(self):
        return self.t.strftime('%Y%m%d')

    @property
    def amz_date(self):
        return self.t.strftime('%Y%m%dT%H%M%SZ')

    @property
    def date(self):
        return self.t.strftime("%A, %d %B %Y %H:%M:%S")

    @property
    def credential_scope(self):
        return "/".join([self.date_stamp, self.region, self.service, 'aws4_request'])

    def get_headers(self, bucket, method, canonical_uri='/', payload='', querystring={}):
        host = bucket + '.s3.amazonaws.com'

        payload_hash = self.__build_payload_hash(payload)

        canonical_querystring = urllib.urlencode(querystring)
        canonical_headers = self.__build_cannonical_headers(host, payload_hash)

        canonical_request = self.__build_cannonical_request(
            method, canonical_uri, canonical_querystring, canonical_headers, self.signed_headers, payload_hash
        )

        string_to_sign = self.__build_string_to_sign(canonical_request)
        signing_key = self.__get_signature_key(self.secret_key)
        signature = self.__build_signature(signing_key, string_to_sign)
        authorization_header = self.__build_authorization_headers(self.signed_headers, signature)

        return {
            'Authorization': authorization_header,
            'Date': self.date,
            'X-Amz-Acl': 'public-read',
            'X-Amz-Content-sha256': payload_hash,
            'X-Amz-Date': self.amz_date
        }

    def __build_cannonical_headers(self, host, payload_hash):
        return "host:{0}\nx-amz-acl:public-read\n" \
               "x-amz-content-sha256:{1}\nx-amz-date:{2}\n".format(host, payload_hash, self.amz_date)

    def __build_authorization_headers(self, signed_headers, signature):
        headers_list = [
            ("Credential", '/'.join([self.access_key, self.credential_scope])),
            ("SignedHeaders", signed_headers),
            ("Signature", signature),
        ]
        headers_str = ", ".join(["=".join([header[0], header[1]]) for header in headers_list])
        return " ".join([self.algorithm, headers_str])

    def __build_payload_hash(self, payload):
        return hashlib.sha256(payload).hexdigest()

    def __build_cannonical_request(self, *args):
        join = '\n'.join(args)
        return join

    def __build_string_to_sign(self, canonical_request):
        elements = [self.algorithm, self.amz_date, self.credential_scope, self.__build_payload_hash(canonical_request)]
        return "\n".join(elements)

    def __build_signature(self, signing_key, string_to_sign):
        return hmac.new(signing_key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

    def __sign(self, key, msg):
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

    def __get_signature_key(self, key):
        k_date = self.__sign(('AWS4' + key).encode('utf-8'), self.date_stamp)
        k_region = self.__sign(k_date, self.region)
        k_service = self.__sign(k_region, self.service)
        k_signing = self.__sign(k_service, 'aws4_request')
        return k_signing
