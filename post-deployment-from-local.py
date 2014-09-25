#!/usr/bin/python

import sys
import os
import requests
import json
import getopt

from os.path import expanduser
from pprint import pprint

def main(args):
    if len(args) < 2:
       print '\nNeed 2 arguments:  <environmentName>  <deploymentName>\n'
       sys.exit(1)
 
    envname = args[1]
    deployname = args[2]
    image = 'ami-94e24cfc'

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
        'name': envname,
        'credentials': credentials,
        'provider': provider
    } 

    # Remember to use different random id's for all virtual instances below if re-run this script within 24 hrs


    deployment = {
  'name' : deployname,
  'managerVirtualInstance' : {
#    'id' : '1c145f51-b33d-44c6-90aa-869493e28bd9',
    'id' : '2c345e59-c43e-54d7-10ba-979593f39ce0',
    'template' : {
      'name' : 'manager',
      'type' : 'm1.xlarge',
      'image' : image,
      'config' : {
        'region' : 'us-east-1',
        'instanceNamePrefix' : deployname,
        'rootVolumeSizeGB' : '30',
        'subnetId' : 'subnet-5b5b962c',
        'securityGroupsIds' : 'sg-895c13ec'
      },
      'tags' : {
        'application' : 'Cloudera Manager 5',
        'owner' : 'hpham'
      }
    }
  },
  'externalDatabases' : { },
  'config' : {
    'customBannerText' : "hpham_ClouderaDirectorServer",
    'username' : 'admin',
    'enableEnterpriseTrial' : 'true',
    'password' : 'admin'
    }
  }

    print 'Doing POST request to http://54.164.165.51:7189/api/environments with:\n'
    pprint(deployment)

    headers = {'content-type': 'application/json'}
    result = requests.post('http://localhost:7189/api/v1/environments/'+envname+'/deployments', data=json.dumps(deployment), headers=headers)

    print '\nGot response:\n'
    pprint(result)
#    pprint(result.json())
    print result.text

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))

