#!/usr/bin/env python
#
# Copyright (c) The University of Edinburgh, 2014.
#
from geosmeta import GeosMETA
from geosmeta import util
import argparse
import json
import sys

if __name__ == '__main__':
        # Get command line arguments
    parser = argparse.ArgumentParser(description="Find gmDocs given a user's query")
    parser.add_argument('--projectName',
                        '-p',
                        required=False,
                        help='Name of the project (required if not in cfg file)')
    parser.add_argument('--file',
                        '-f',
                        required=False,
                        help='filename')
    parser.add_argument('--searchField',
                        '-s',
                        choices=['input_files', 'output_files'],
                        required=True,
                        help='output_files or input_files')
    
    parser.add_argument('--config-file','-C',metavar='FILE',help="read configuration from FILE: default:~/.geosmeta/geosmeta.cfg")
    args = parser.parse_args()
    projectName = args.projectName

    gm = GeosMETA(configFilePath=args.config_file)
        # Submit the query
    try:
                (ndocs,idlist) = gm.findFileUse(projectName, args.file,args.searchField)

                print("number of current docs %d"%ndocs)
                for idoc in idlist:
                      print(idoc)
                sys.stderr.write('The end\n' )
                sys.exit(0)
    except Exception as err:
            sys.stderr.write('Error submitting the query:\n')
            sys.stderr.write('%s\n' % str(err))
            sys.exit(1)
    else:
            sys.stdout.write('Received activities:\n\n')
            sys.exit(0)
