#!/usr/bin/python

import sys
import os
import requests
import json

from os.path import expanduser
from pprint import pprint

def main(args):
    if len(args) < 4:
        print '\nNeed 4 arguments:  <environmentName>  <deployName>  <clusterName>  <ami-image>\n'
        sys.exit(1)

    envname = args[1] 
    deployname = args[2] 
    clustername = args[3] 
    image = args[4]

    print '\nEnvName = '+envname+'\n'
    print '\nDeployName = '+deployname+'\n'
    print '\nClusterName = '+clustername+'\n'
    print '\nAMI image = '+image+'\n'

    credentials = {
        'username': 'root', # os.environ['USER'],
        'port': 22,
        'privateKey': file(expanduser('~/hpham_aws.pem')).read()
    }

    provider = {
        'id': 'aws',
        'config': {
            'keyName': 'hpham_aws',
            'accessKeyId = ': os.environ['AWS_ACCESS_KEY_ID'],
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

    accessKeyId = os.environ['AWS_ACCESS_KEY_ID']
    secretAccessKey = os.environ['AWS_SECRET_ACCESS_KEY']
    region = os.environ['AWS_DEFAULT_REGION']

    cluster = {
  "name" : clustername,
  "productVersions" : {
    "CDH" : "5.1.2"
  },
  "services" : [ "HDFS", "YARN", "ZOOKEEPER", "HIVE", "OOZIE", "HUE", "SPARK" ],
  "servicesConfigs" : {
    "HIVE" : { },
    "SPARK" : { },
    "ZOOKEEPER" : { },
    "OOZIE" : { },
    "HDFS" : { },
    "YARN" : { }
  },
  "virtualInstanceGroups" : {
    "gateway" : {
      "name" : "gateway",
      "virtualInstances" : [ {
        "id" : "6e3609d3-6gdf-5be0-9836-21984e80e3cd",
        "template" : {
          "name" : "gateway",
          "type" : "m3.2xlarge",
          "image" : image,
          "bootstrapScript" : "#!/bin/sh\nexit 0\n",
          "config" : {
            "instanceNamePrefix" : clustername,
            "region" : region,
            "rootVolumeSizeGB" : "50",
            "keyName" : "hpham_aws",
            "secretAccessKey" : secretAccessKey,
            "publishAccessKeys" : "false",
            "accessKeyId" : accessKeyId,
            "subnetId" : "subnet-5b5b962c",
            "securityGroupsIds" : "sg-895c13ec"
          },
          "tags" : {
            "owner" : "root",
            "group" : "gateway"
          }
        }
      } ],
      "minCount" : 1,
      "serviceTypeToRoleTypes" : {
        "YARN" : [ "GATEWAY" ],
        "HUE" : [ "HUE_SERVER" ],
        "OOZIE" : [ "OOZIE_SERVER" ],
        "HIVE" : [ "HIVESERVER2", "GATEWAY" ],
        "HDFS" : [ "HTTPFS", "GATEWAY" ]
      },
      "roleTypesConfigs" : { }
    },
    "master1" : {
      "name" : "master1",
      "virtualInstances" : [ {
        "id" : "g5272404-7b13-5bec-bc79-c7g7bebfh9e9",
        "template" : {
          "name" : "master1",
          "type" : "m3.2xlarge",
          "image" : image,
          "bootstrapScript" : "#!/bin/sh\nexit 0\n",
          "config" : {
            "instanceNamePrefix" : clustername,
            "region" : region,
            "rootVolumeSizeGB" : "50",
            "keyName" : "hpham_aws",
            "secretAccessKey" : secretAccessKey,
            "publishAccessKeys" : "false",
            "accessKeyId" : accessKeyId,
            "subnetId" : "subnet-5b5b962c",
            "securityGroupsIds" : "sg-895c13ec"
          },
          "tags" : {
            "owner" : "root",
            "group" : "master"
          }
        }
      } ],
      "minCount" : 1,
      "serviceTypeToRoleTypes" : {
        "HDFS" : [ "NAMENODE", "JOURNALNODE" ],
        "ZOOKEEPER" : [ "SERVER" ]
      },
      "roleTypesConfigs" : { }
    },
    "master3" : {
      "name" : "master3",
      "virtualInstances" : [ {
        "id" : "540ef592-5b58-5924-c8b3-7c3d41a9a4fg",
        "template" : {
          "name" : "master3",
          "type" : "m3.2xlarge",
          "image" : image,
          "bootstrapScript" : "#!/bin/sh\nexit 0\n",
          "config" : {
            "instanceNamePrefix" : clustername,
            "region" : region,
            "rootVolumeSizeGB" : "50",
            "keyName" : "hpham_aws",
            "secretAccessKey" : secretAccessKey,
            "publishAccessKeys" : "false",
            "accessKeyId" : accessKeyId,
            "subnetId" : "subnet-5b5b962c",
            "securityGroupsIds" : "sg-895c13ec"
          },
          "tags" : {
            "owner" : "root",
            "group" : "master"
          }
        }
      } ],
      "minCount" : 1,
      "serviceTypeToRoleTypes" : {
        "ZOOKEEPER" : [ "SERVER" ],
        "HIVE" : [ "HIVEMETASTORE" ],
        "SPARK" : [ "SPARK_MASTER" ],
        "HDFS" : [ "BALANCER", "JOURNALNODE" ],
        "YARN" : [ "JOBHISTORY" ]
      },
      "roleTypesConfigs" : { }
    },
    "master2" : {
      "name" : "master2",
      "virtualInstances" : [ {
        "id" : "7396f34e-051d-56r7-b213-2025ef8943f3",
        "template" : {
          "name" : "master2",
          "type" : "m3.2xlarge",
          "image" : image,
          "bootstrapScript" : "#!/bin/sh\nexit 0\n",
          "config" : {
            "instanceNamePrefix" : clustername,
            "region" : region,
            "rootVolumeSizeGB" : "50",
            "keyName" : "hpham_aws",
            "secretAccessKey" : secretAccessKey,
            "publishAccessKeys" : "false",
            "accessKeyId" : accessKeyId,
            "subnetId" : "subnet-5b5b962c",
            "securityGroupsIds" : "sg-895c13ec"
          },
          "tags" : {
            "owner" : "root",
            "group" : "master"
          }
        }
      } ],
      "minCount" : 1,
      "serviceTypeToRoleTypes" : {
        "YARN" : [ "RESOURCEMANAGER" ],
        "ZOOKEEPER" : [ "SERVER" ],
        "HDFS" : [ "SECONDARYNAMENODE", "JOURNALNODE" ]
      },
      "roleTypesConfigs" : { }
    },
    "workers" : {
      "name" : "workers",
      "virtualInstances" : [ {
        "id" : "414b487d-990a-4b8c-05b1-b345cbe686h2",
        "template" : {
          "name" : "workers",
          "type" : "m3.2xlarge",
          "image" : image,
          "bootstrapScript" : "#!/bin/sh\nexit 0\n",
          "config" : {
            "instanceNamePrefix" : clustername,
            "region" : region,
            "rootVolumeSizeGB" : "50",
            "keyName" : "hpham_aws",
            "secretAccessKey" : secretAccessKey,
            "publishAccessKeys" : "false",
            "accessKeyId" : accessKeyId,
            "subnetId" : "subnet-5b5b962c",
            "securityGroupsIds" : "sg-895c13ec"
          },
          "tags" : {
            "owner" : "root",
            "group" : "worker"
          }
        }
      }, {
        "id" : "286g6d7h-c74g-4bc9-10b9-g1hac3548h20",
        "template" : {
          "name" : "workers",
          "type" : "m3.2xlarge",
          "image" : image,
          "bootstrapScript" : "#!/bin/sh\nexit 0\n",
          "config" : {
            "instanceNamePrefix" : clustername,
            "region" : region,
            "rootVolumeSizeGB" : "50",
            "keyName" : "hpham_aws",
            "secretAccessKey" : secretAccessKey,
            "publishAccessKeys" : "false",
            "accessKeyId" : accessKeyId,
            "subnetId" : "subnet-5b5b962c",
            "securityGroupsIds" : "sg-895c13ec"
          },
          "tags" : {
            "owner" : "root",
            "group" : "worker"
          }
        }
      }, {
        "id" : "ru0k2be1-19jc-89u4-ilka-1luv1931ha58",
        "template" : {
          "name" : "workers",
          "type" : "m3.2xlarge",
          "image" : image,
          "bootstrapScript" : "#!/bin/sh\nexit 0\n",
          "config" : {
            "instanceNamePrefix" : clustername,
            "region" : region,
            "rootVolumeSizeGB" : "50",
            "keyName" : "hpham_aws",
            "secretAccessKey" : secretAccessKey,
            "publishAccessKeys" : "false",
            "accessKeyId" : accessKeyId,
            "subnetId" : "subnet-5b5b962c",
            "securityGroupsIds" : "sg-895c13ec"
          },
          "tags" : {
            "owner" : "root",
            "group" : "worker"
          }
        }
      }, {
        "id" : "fe4899de-gba7-78b7-99a3-5ah7u2685f2g",
        "template" : {
          "name" : "workers",
          "type" : "m3.2xlarge",
          "image" : image,
          "bootstrapScript" : "#!/bin/sh\nexit 0\n",
          "config" : {
            "instanceNamePrefix" : clustername,
            "region" : region,
            "rootVolumeSizeGB" : "50",
            "keyName" : "hpham_aws",
            "secretAccessKey" : secretAccessKey,
            "publishAccessKeys" : "false",
            "accessKeyId" : accessKeyId,
            "subnetId" : "subnet-5b5b962c",
            "securityGroupsIds" : "sg-895c13ec"
          },
          "tags" : {
            "owner" : "root",
            "group" : "worker"
          }
        }
      } ],
      "minCount" : 4,
      "serviceTypeToRoleTypes" : {
        "HDFS" : [ "DATANODE" ],
        "SPARK" : [ "SPARK_WORKER" ],
        "YARN" : [ "NODEMANAGER" ],
        "HIVE" : [ "GATEWAY" ]
      },
      "roleTypesConfigs" : { }
    }
  },
  "externalDatabases" : { }
}


 

    print 'Doing POST request to http://launchpad-server:8080/api/environments with:\n'
    pprint(cluster)

    headers = {'content-type': 'application/json'}
    result = requests.post('http://localhost:8080/api/v1/environments/'+envname+'/deployments/'+deployname+'/clusters', data=json.dumps(cluster), headers=headers)

    print '\nGot response:\n'
    pprint(result)
  #pprint(result.json())
    print result.text

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))

