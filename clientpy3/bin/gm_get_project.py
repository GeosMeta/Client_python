#!/usr/bin/env python
#
# Copyright (c) The University of Edinburgh, 2014.
#
from geosmeta import GeosMETA
from geosmeta import util
import argparse
import sys
import json

if __name__ == '__main__':
    # Get command line arguments
    parser = argparse.ArgumentParser(description="Get project details from the GeosMeta system")
    parser.add_argument('--project',
                        '-p',
                        required=False,
                        help='Name of the project')
    parser.add_argument('--config-file','-C',metavar='FILE',help="read configuration from FILE: default:~/.geosmeta/geosmeta.cfg")
    args = parser.parse_args()

    project_id = args.project

    gm = GeosMETA(configFilePath=args.config_file)
    response=True
    if (response):
        # Get user details
        print("Getting project details")
        try:
            resultJSON = gm.getProject(project_id=project_id)
                                      
        except Exception as err:
            sys.stderr.write('Error getting project:\n')
            sys.stderr.write('%s\n' % str(err))
            sys.exit(1)
        else:
            sys.stdout.write('Got project details:\n\n')
            sys.stdout.write(json.dumps(resultJSON,
                                        indent=2,
                                        sort_keys=True))

        if (project_id):
            print("\nGetting project roles")
            try:
                rolesJSON = gm.getProjectRoles(project_id)
            except Exception as err:
                sys.stderr.write('\nError getting project roles:\n')
                sys.stderr.write('%s\n' % str(err))
                sys.exit(1)
            else:
                sys.stdout.write('\nGot project roles:\n\n')
                sys.stdout.write(json.dumps(rolesJSON,
                                            indent=2,
                                            sort_keys=True))

        sys.exit(0)
    else:
        sys.stdout.write('Not getting project details\n')
        sys.exit(0)
