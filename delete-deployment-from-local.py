#!/usr/bin/python

import sys
import os
import requests
import json

from os.path import expanduser
from pprint import pprint

def main(args):
    if len(args) < 2:
       print '\nNeed 2 arguments: <environmentName>  <deployName 2 be deleted>\n'
       sys.exit(1)

    envname = args[1]
    deployname = args[2]
    image = "ami-c447e5ac"

    credentials = {
        'username': 'root', # os.environ['USER'],
        'port': 22,
        'privateKey': file(expanduser('~/hpham_aws.pem')).read()
    }

    provider = {
        'id': 'aws',
        'config': {
            'accessKeyId': os.environ['AWS_ACCESS_KEY_ID'],
            'secretAccessKey': os.environ['AWS_SECRET_ACCESS_KEY'],
            'region': os.environ['AWS_DEFAULT_REGION'],
            'image': image
        }
    }

    environment = {
        'name': envname,
        'credentials': credentials,
        'provider': provider
    } 

    print "Doing DELETE request to http://launchpad-server:7189/api/environments with:\n"
    pprint(environment)
    pprint(envname)

    headers = {'content-type': 'application/json'}
    #result = requests.get('http://localhost:7189/api/environments', data=json.dumps(environment), headers=headers)
    querystr = 'http://localhost:7189/api/v1/environments/'+envname+'/deployments/'+deployname
    pprint(querystr)

    #result = requests.delete('http://localhost:7189/api/v1/environments/'+envname+'/deployments/'+deployname)
    result = requests.delete(querystr)

    print "\nGot response:\n"
    pprint(result)
    print result.text

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))

