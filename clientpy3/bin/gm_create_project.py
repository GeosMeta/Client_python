#!/usr/bin/env python
#
# Copyright (c) The University of Edinburgh, 2014.
#
import argparse
from geosmeta import GeosMETA
import sys

if __name__ == '__main__':
    # Get command line arguments
    parser = argparse.ArgumentParser(description="Add a project to the GeosMeta system")
    parser.add_argument('--project_id',
                        '-p',
                        required=True,
                        help='Id of the Project - no spaces allowed')
    parser.add_argument('--description',
                        '-d',
                        required=False,
                        help='A short description of the Project')
    parser.add_argument('--comment',
                        '-c',
                        required=False,
                        help='Additional comments')
    parser.add_argument('--researchgroup',
                        '-r',
                        required=True,
                        help='Research Group this project belongs to')
    parser.add_argument('--config-file','-C',metavar='FILE',help="read configuration from FILE: default:~/.geosmeta/geosmeta.cfg")
    args = parser.parse_args()

    project_id = args.project_id
    description = args.description
    comment = args.comment
    researchGroup = args.researchgroup

    gm = GeosMETA(configFilePath=args.config_file)

    # Only proceed if project_id, username and research group is provided
    if (project_id and researchGroup):
        # Create a Research Group
        #try:
        #    import pdb;pdb.set_trace()
        result = gm.addProject(project_id, researchGroup, description, comment)
        #except Exception as err:
            #sys.stderr.write('Error creating Project\n')
            #sys.stderr.write('%s\n' % str(err))
            #sys.exit(1)
        #else:
            #sys.stdout.write('Project was created successfully, Project ID:' + str(result) + '\n')
            #sys.exit(0)
    #else:
        #sys.stdout.write('Not creating Project\n')
        #sys.exit(0)
