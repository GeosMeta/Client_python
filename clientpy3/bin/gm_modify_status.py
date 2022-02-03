#!/usr/bin/env python
#
# Copyright (c) The University of Edinburgh, 2014.
#
from geosmeta import GeosMETA
import argparse
import sys
import json

if __name__ == '__main__':
    # Get command line arguments
    parser = argparse.ArgumentParser(description= \
             """"Changes the status field of the gmDoc, and optionally 
             the tree of downstream documents (connected by output/input files)
             """)
    parser.add_argument('--id',
                        '-i',
                        required=True,
                        help=' the gmDoc _id (required)')
    parser.add_argument('--projectName',
                        '-p',
                        required=False,
                        help='Name of project (required- can be set in cfg file)')
    parser.add_argument('--newStatus',
                        '-n',
                        choices=['C','E'],
                        required=True,
                        help=' C for current,E for error')

    parser.add_argument('--recursive',
                        '-r',
                        required=False,
                        default=False,
                        action="store_true",
                        help="Change status for all downstream documents")

    parser.add_argument('--message',
                        '-m',
                        required=True,
                        help='few words to explain why change is being done')
    parser.add_argument('--config-file','-C',metavar='FILE',help="read configuration from FILE: default:~/.geosmeta/geosmeta.cfg")

    args = parser.parse_args()

    docId = args.id
    projectName = args.projectName
    goDownStream = args.recursive
    message = args.message
    newStatus= args.newStatus

    gm = GeosMETA(configFilePath=args.config_file)


        #first get the document and then extract the etag
    try:
            resultJSON = gm.getActivity(projectName, docId)
    except Exception as err:
            sys.stderr.write('Error retrieving the etag:\n')
            sys.stderr.write('%s\n' % str(err))
            sys.exit(1)
    else:
            sys.stdout.write('Etag retrieved successfully: \n')
            activityID = resultJSON['_id']
            activityEtag = resultJSON['_etag']
            print('Etag: ' + activityEtag)
            print('_id:' + activityID)

    '''
           API responses include a ETag header which also allows for proper concurrency control. An ETag is a hash value
representing the current state of the resource on the server. Consumers are not allowed to edit (PATCH or PUT) or
delete (DELETE) a resource unless they provide an up-to-date ETag for the resource they are attempting to edit. This
prevents overwriting items with obsolete versions
https://readthedocs.org/projects/eve/downloads/pdf/latest/, 5.3.32, pg 22
    '''
        # Now update the activity using its _id, _etag and the change to be made.
    try:
            result = gm.updateDocStatus(activityID, activityEtag,
                                        newStatus,message, goDownStream)
            print(result)

    except Exception as err:
            sys.stderr.write('Error updating the gmDoc status:\n')
            sys.stderr.write('%s\n' % str(err))
            sys.exit(1)

    else:
            sys.stdout.write('gmDoc status was updated successfully, ID:' + str(result) + '\n')
            sys.stdout.write('retrieving updated gmDoc:\n')
            newDoc=gm.getActivity(projectName, docId)
            sys.stdout.write(json.dumps(newDoc,
                                            indent=2,
                                            sort_keys=True))
            sys.exit(0)

