#!/usr/bin/env python
#
# Copyright (c) The University of Edinburgh, 2014.
#
from geosmeta import GeosMETA
from geosmeta  import util
import argparse
import sys
import json

if __name__ == '__main__':
    # Get command line arguments
    parser = argparse.ArgumentParser(description= \
                """Get gmDoc(s) from the GeosMeta system: 
                either all in a project, or a doc with a specified _id
                """)
    parser.add_argument('--id',
                        '-i',
                        default=None,
                        required=False,
                        help='id of the document')
    parser.add_argument('--All',
                        '-A',
                        required=False,
                        default=False,
                        action="store_true",
                        help='All documents in this project')
    parser.add_argument('--project',
                        '-p',
                        required=False,
                        default=None,
                        help='Name of the project (can be in cfg file)')
    parser.add_argument('--doctype',
                         '-d',
                         required=False,
                         default='A',
                         choices=['A','E','F'],
                         help='A(ctivity)- default, E(ntity), F(ile)')
    parser.add_argument('--selectedField',
                        '-s',
                        required=False,
                        action='append',
                        default=None,
                        help='Field name to append to selected fields list')
    parser.add_argument('--config-file',
                        '-C',
                        metavar='FILE',
                        help="read configuration from FILE: default:~/.geosmeta/geosmeta.cfg")
    args = parser.parse_args()

    id = args.id
    projectName = args.project
    

    if id is None and not args.All:
       print("either choose an id or set -A")
       sys.exit(1)

    gm = GeosMETA(configFilePath=args.config_file)

        # Get user details
    try:
        selFields=args.selectedField
        if id: # is not None:
            resultJSON = gm.getDoc(args.doctype,projectName, id, selFields)
        elif args.All:
            print("args option set for all docs")
            resultJSON = gm.getProjectCollection(args.doctype, projectName)
    except Exception as err:
                print('Error getting gmDocs:',err,file=sys.stderr)
                sys.exit(1)
    else:
         sys.stdout.write('Got gmDoc details:\n\n')
         sys.stdout.write(json.dumps(resultJSON,
                                            indent=2,
                                            sort_keys=True))
         if id is None: # getting all documents
                               # get the other pages
           try:
              while ('next' in resultJSON['_links']):
                   mynext=resultJSON['_links']['next']['href']

                   print("retrieving %s\n"%(mynext))

                   resultJSON=gm.getHREF(mynext,projectName,
                                         selectedFields=selFields)
                   print("\n no. docs: %d\n"%(len(resultJSON['_items'])))

                   for itm in resultJSON['_items']:
                              print(itm['_id'])
                           #print "resultJSON %s\n"%(resultJSON)

                           #sys.stdout.write(json.dumps(resultJSON,
                                            #indent=2,
                                            #sort_keys=True))
           except Exception as err:
                         sys.stderr.write('next page error %s\n' % str(err))
         sys.stdout.write('The end\n' )
