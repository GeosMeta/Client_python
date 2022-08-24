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
         """ For gmDoc specified by its id, creates/updates a single field""")
    parser.add_argument('--id',
                        '-i',
                        required=True,
                        help=' the gmDoc _id (required)')
    parser.add_argument('--projectName',
                        '-p',
                        required=False,
                        help='Name of project (required- can be set in cfg file)')
    parser.add_argument('--field',
                        '-f',
                        required=True,
                        help='Name of the field (required) e.g.  gmdata.adict')
    parser.add_argument('--value',
                        '-v',
                        required=True,
                        help="""Value for the field (required): can be 
ingle value, or a dict in quotes""")
    parser.add_argument('--config-file','-C',metavar='FILE',help="read configuration from FILE: default:~/.geosmeta/geosmeta.cfg")
    args = parser.parse_args()

    docId = args.id
    projectName = args.projectName
    field = args.field
    value = args.value

    gm = GeosMETA(configFilePath=args.config_file)

    if docId:

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


        # Now update the activity using its _id, _etag and the change to be made.
        try:
            result = gm.updateActivity(activityID, activityEtag, field, value)
            print(result)
        except Exception as err:
            sys.stderr.write('Error updating the activity:\n')
            sys.stderr.write('%s\n' % str(err))
            sys.exit(1)

        else:
            sys.stdout.write('Activity was updated successfully, Activity ID:' + str(result) + '\n')
            sys.exit(0)
    else:
        sys.stdout.write('Not updating the activity\n')
        sys.exit(0)

