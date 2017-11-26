#!/usr/bin/env python
from __future__ import print_function

import argparse
import base64
import hashlib
import hmac
import sys
from datetime import datetime
import json
import requests 

def sign(key, val):
    return hmac.new(key, val.encode('utf-8'), hashlib.sha256).digest()

def getSignatureKey(key, dateStamp, regionName, serviceName):
    kDate = sign(("AWS4" + key).encode("utf-8"), dateStamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, "aws4_request")
    return kSigning

"""
Updates the AWS_SIGNING_KEY and AWS_KEY_SCOPE env vars in Heroku.
This is required as the signing keys are only valid for a week.
"""
def updateSignature(hk, signature, scope):
    url = "https://api.heroku.com/apps/vod/config-vars"
    payload = {'AWS_SIGNING_KEY': signature, 'AWS_KEY_SCOPE': scope}
    headers = {
        'authorization': "Bearer " + hk,
        'content-type': "application/json",
        'accept': "application/vnd.heroku+json; version=3",
    }

    response = requests.patch(url, data=json.dumps(payload), headers=headers)
    return response.status_code

def cmdline_parser():
    parser = argparse.ArgumentParser(description="Generate AWS S3 signing key in it's base64 encoded form")
    parser.add_argument("-k", "--secret-key", required=True, help='The secret key generated using AWS IAM. Do not confuse this with the access key id')
    parser.add_argument("-hk", "--heroku-key", required=True, help='Heroku API Key')
    parser.add_argument("-r", "--region", required=True, help='The AWS region where this key would be used. Example: us-east-1')
    parser.add_argument("-s", "--service", help='The AWS service for which this key would be used. Example: s3')
    parser.add_argument("-d", "--date", help='The date on which this key is generated in yyyymmdd format')
    parser.add_argument("--no-base64", action='store_true', help='Disable output as a base64 encoded string. This NOT recommended')
    parser.add_argument("-v", "--verbose", action='store_true', help='Produce verbose output on stderr')
    return parser.parse_args()

if __name__ == "__main__":
    args = cmdline_parser()
    verbose = args.verbose

    ymd = args.date
    if ymd is None:
        now = datetime.utcnow().date()
        ymd = '%04d%02d%02d' % (now.year, now.month, now.day)
        if verbose:
            print('The auto-selected date is %s' % ymd,  file=sys.stderr)

    service = args.service
    if service is None:
        service = 's3'
        if verbose:
            print('The auto-selected service is %s' % service,  file=sys.stderr)

    region = args.region
    signature = getSignatureKey(args.secret_key, ymd, region, service)

    if args.no_base64:
        signature = signature.decode('latin_1')
    else:
        signature = base64.b64encode(signature).decode('ascii')

    print('Updating signature...')
    scope = '%s/%s/%s/aws4_request' % (ymd, region, service)
    s = updateSignature(args.heroku_key, signature, scope)
    print(s)
    # print(signature)
    # print('%s/%s/%s/aws4_request' % (ymd, region, service))
