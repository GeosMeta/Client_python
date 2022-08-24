#!/usr/bin/env python
#
# Copyright (c) The University of Edinburgh, 2014.
#
from .api import GeosMETA
from .util import queryYesNo
import argparse
import sys
import json


def main():
    # Get command line arguments
    parser = argparse.ArgumentParser(description="Get research group details from the GeosMeta system")
    parser.add_argument('--researchgroup',
                        '-r',
                        required=False,
                        help='Name of the research group to get details for')
    parser.add_argument('--config-file','-C',metavar='FILE',help="read configuration from FILE: default:~/.geosmeta/geosmeta.cfg")
    args = parser.parse_args()

    researchGroupName = args.researchgroup

    gm = GeosMETA(configFilePath=args.config_file)

    # Prompt user for confirmation
    if (researchGroupName):
        question = "Get details of %s?"\
               % (researchGroupName)
    else:
        question = "Get all research groups?"

    response = queryYesNo(question)

    if (response):
        # Get research group details
        print("Getting research group details")
        try:
            resultJSON = gm.getResearchGroups(researchGroupName=researchGroupName)
        except Exception as err:
            sys.stderr.write('Error getting research groups:\n')
            sys.stderr.write('%s\n' % str(err))
            sys.exit(1)
        else:
            sys.stdout.write('Got research group details:\n\n')
            sys.stdout.write(json.dumps(resultJSON,
                                        indent=2,
                                        sort_keys=True))
            sys.exit(0)
    else:
        sys.stdout.write('Not getting reseach group details details\n')
        sys.exit(0)


if __name__ == '__main__':
    main()
