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
    "CDH" : "5.1.3"
  },
  "services" : [ "HDFS", "YARN", "ZOOKEEPER", "HIVE", "OOZIE", "HUE", "SPARK" ],
  "servicesConfigs" : {
    "HIVE" : { },
    "SPARK" : { },
    "ZOOKEEPER" : {      
      "zookeeper_datadir_autocreate" : "true"
    },
    "OOZIE" : { },
    "HDFS" : { 
      "dfs_permissions" : "true",
      "dfs_block_size" : "134217728",
      "dfs_webhdfs_enabled" : "true",
      "dfs_umaskmode" : "022"
    },
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
      "roleTypesConfigs" : { 
        "HIVE" : {
          "HIVESERVER2" : {
            "hiveserver2_java_heapsize" : "1073741824"
          },
          "GATEWAY" : { }
        },
        "HUE" : {
          "HUE_SERVER" : { }
        },
        "OOZIE" : {
          "OOZIE_SERVER" : {
            "oozie_java_heapsize" : "1073741824"
          }
        },
        "HDFS" : {
          "HTTPFS" : { },
          "GATEWAY" : { }
        },
        "YARN" : {
          "GATEWAY" : {
            "mapred_submit_replication" : "3",
            "yarn_app_mapreduce_am_resource_cpu_vcores" : "1",
            "mapred_reduce_tasks" : "3",
            "io_sort_mb" : "128",
            "mapreduce_reduce_memory_mb" : "1024",
            "mapreduce_reduce_cpu_vcores" : "1",
            "mapreduce_reduce_java_opts_max_heap" : "825955249",
            "mapreduce_map_memory_mb" : "1024",
            "mapreduce_map_java_opts_max_heap" : "825955249",
            "mapreduce_map_cpu_vcores" : "1",
            "yarn_app_mapreduce_am_resource_mb" : "1024"
          }
        }
      }
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
      "roleTypesConfigs" : { 
        "ZOOKEEPER" : {
          "SERVER" : {
            "dataLogDir" : "/data1/log/zookeeper",
            "maxClientCnxns" : "100",
            "dataDir" : "/data0/zookeeper",
            "zookeeper_server_java_heapsize" : "1073741824"
          }
        },
        "HDFS" : {
          "NAMENODE" : {
            "namenode_java_heapsize" : "1073741824",
            "dfs_name_dir_list" : "/data0/nn"
          },
          "JOURNALNODE" : {
            "dfs_journalnode_edits_dir" : "/data0/jn"
          }
        }
      }
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
      "roleTypesConfigs" : { 
        "HIVE" : {
          "HIVEMETASTORE" : {
            "hive_metastore_java_heapsize" : "1073741824"
          }
        },
        "SPARK" : {
          "SPARK_MASTER" : {
            "master_max_heapsize" : "1073741824"
          }
        },
        "ZOOKEEPER" : {
          "SERVER" : {
            "dataLogDir" : "/data1/log/zookeeper",
            "maxClientCnxns" : "100",
            "dataDir" : "/data0/zookeeper",
            "zookeeper_server_java_heapsize" : "1073741824"
          }
        },
        "HDFS" : {
          "BALANCER" : { },
          "JOURNALNODE" : {
            "dfs_journalnode_edits_dir" : "/data0/jn"
          }
        },
        "YARN" : {
          "JOBHISTORY" : {
            "mr2_jobhistory_java_heapsize" : "1073741824"
          }
        }
      }
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
      "roleTypesConfigs" : { 
        "ZOOKEEPER" : {
          "SERVER" : {
            "dataLogDir" : "/data1/log/zookeeper",
            "maxClientCnxns" : "100",
            "dataDir" : "/data0/zookeeper",
            "zookeeper_server_java_heapsize" : "1073741824"
          }
        },
        "HDFS" : {
          "SECONDARYNAMENODE" : {
            "secondary_namenode_java_heapsize" : "1073741824",
            "fs_checkpoint_dir_list" : "/data0/snn"
          },
          "JOURNALNODE" : {
            "dfs_journalnode_edits_dir" : "/data0/jn"
          }
        },
        "YARN" : {
          "RESOURCEMANAGER" : {
            "yarn_scheduler_increment_allocation_mb" : "256",
            "yarn_scheduler_maximum_allocation_vcores" : "4",
            "resource_manager_java_heapsize" : "1073741824",
            "yarn_scheduler_minimum_allocation_mb" : "1024",
            "yarn_scheduler_minimum_allocation_vcores" : "1",
            "yarn_scheduler_maximum_allocation_mb" : "4096"
          }
        }
      }
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
      "roleTypesConfigs" : { 
        "HIVE" : {
          "GATEWAY" : { }
        },
        "SPARK" : {
          "SPARK_WORKER" : {
            "executor_total_max_heapsize" : "8589934592",
            "worker_max_heapsize" : "1073741824",
            "worker_webui_port" : "18081",
            "rm_io_weight" : "500",
            "worker_port" : "7078",
            "process_auto_restart" : "true",
            "rm_cpu_shares" : "1024"
          }
        },
        "HDFS" : {
          "DATANODE" : {
            "datanode_java_heapsize" : "1073741824",
            "dfs_datanode_du_reserved" : "10737418240",
            "dfs_datanode_failed_volumes_tolerated" : "1"
          }
        },
        "YARN" : {
          "NODEMANAGER" : {
            "yarn_nodemanager_resource_memory_mb" : "4096",
            "yarn_nodemanager_resource_cpu_vcores" : "4",
            "node_manager_java_heapsize" : "1073741824"
          }
        }
      }
    }
  },
  "externalDatabases" : { }
}


 

    print 'Doing POST request to http://launchpad-server:7189/api/environments with:\n'
    pprint(cluster)

    headers = {'content-type': 'application/json'}
    result = requests.post('http://localhost:7189/api/v1/environments/'+envname+'/deployments/'+deployname+'/clusters', data=json.dumps(cluster), headers=headers)

    print '\nGot response:\n'
    pprint(result)
  #pprint(result.json())
    print result.text

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))

