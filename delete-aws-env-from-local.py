#!/usr/bin/python

import sys
import os
import requests
import json

from os.path import expanduser
from pprint import pprint

def main(args):
    name = args[1] if len(args) == 2 else "hpham-0912-lpadsrv"
    image = args[2] if len(args) == 3 else "ami-c447e5ac"

    credentials = {
        'username': 'root', # os.environ['USER'],
        'port': 22,
        'privateKey': file(expanduser('~/hpham_aws.pem')).read()
    }

    provider = {
        'id': 'aws',
        'config': {
            'keyName': 'hpham_aws',
            'accessKeyId': os.environ['AWS_ACCESS_KEY_ID'],
            'secretAccessKey': os.environ['AWS_SECRET_ACCESS_KEY'],
            'region': os.environ['AWS_DEFAULT_REGION'],
            'image': image
        }
    }

    environment = {
        'name': name,
        'credentials': credentials,
        'provider': provider
    } 

    print "Doing DELETE request to http://launchpad-server:7189/api/environments with:\n"
    pprint(environment)

    headers = {'content-type': 'application/json'}
    #result = requests.post('http://localhost:7189/api/v1/environments', data=json.dumps(environment), headers=headers)
    result = requests.delete('http://localhost:7189/api/v1/environments/'+name)

    print "\nGot response:\n"
    pprint(result)
#    pprint(result.json())
    print result.text

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))

