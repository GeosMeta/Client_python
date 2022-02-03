#!/usr/bin/env python
#
# Copyright (c) The University of Edinburgh, 2014.
#
from geosmeta import GeosMETA
import argparse
import sys
import json


def addTheDoc(project_id,configFile, metaFields):
    """
    Function to add either a jsonfile or a python dictionary as 
    a new gmDoc
    :param project_id: Can be None unless passed in from command line argument
    :param configFile: can be None unless passed in
    :param metaFields: either a python dictionary or a jsonfile
    """

    gm = GeosMETA(configFilePath=configFile)
    try:
            result = gm.addDoc(project_id, metaFields)
    except Exception as err:
            sys.stderr.write('Error creating gmDoc:\n')
            sys.stderr.write('%s\n' % str(err))
            raise #        sys.exit(1)

    else:
          return result
    



def testAddDocFromDict(project_id, configFile):
    """
    A test function to exercise teh python dictionary option
    Hardcodes a dict then sends it
    """
    import os
    adict=dict()
    adict['trial']=1
    adict['hostname']=os.environ["HOSTNAME"]
    adict['cwd']=os.getcwd()
    adict['aparameter']='5'
    adict['input_files']=['anew.file']
    adict['output_files']=[['a.dat',{'checksum':'4a', 'otherstuff':'albert'}],['b.dat',{'checksum':'4b', 'otherstuff':'bertie'}]]
    return addTheDoc(project_id,configFile, adict)


    

if __name__ == '__main__':
    # Get command line arguments
    desc="""Uploads a gmDoc using the GeosMeta system - 
            usually used if a json file exists; 
            option -t is for testing the dictioanry interface. 
            Often this code will be reused in applications."""
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('--project',
                        '-p',
                        default=None,
                        required=False,
                        help='Name of the project (can be in cfg file)')

    parser.add_argument('--jsonFile',
                        '-j',
                        required=False,
                        default=None,
                        help='json file containing additional data')

    parser.add_argument('--testDict', 
                        '-t',
                        required=False,
                        action="store_true",
                        help='force test use of a python dictionary instead of JSON file')

    parser.add_argument('--configfile',
                       '-C',
                       metavar='FILE',
         help="read configuration from FILE: default:~/.geosmeta/geosmeta.cfg")

    args = parser.parse_args()

    jsonFile = args.jsonFile
    project=args.project

    if not args.testDict and jsonFile is None:
         print("choose -t to test with dict, or -j jsonfile")
         sys.exit(1)

    configFile=args.configfile

    try:
        if args.testDict:
           print("write test dictionary")
           result = testAddDocFromDict(project, configFile)
        else:
           print("send JSONfile %s\n "%jsonFile)
           result = addTheDoc(project,configFile, jsonFile)

    
    except Exception as err:
            sys.stderr.write('Error creating activity:\n')
            sys.stderr.write('%s\n' % str(err))

    else:
        sys.stdout.write('gmdoc  was created successfully\n')
        sys.stdout.write('gmdoc  id %s\n'%result['_id'])
       # sys.stdout.write(json.dumps(result,
                                           #indent=2,
                                           #sort_keys=True) )
       #sys.stdout.write('\n exit successfully\n')
        sys.exit(0)
  
