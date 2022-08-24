#!/usr/bin/env python
#
# Copyright (c) The University of Edinburgh, 2014.
#
from .api import GeosMETA
import argparse
import json
import sys


def main():
        # Get command line arguments
    parser = argparse.ArgumentParser(description="Find gmDocs given a user's query")
    parser.add_argument('--query',
                        '-q',
                        required=False,
                        help='key-value search query (required)')
    parser.add_argument('--projectName',
                        '-p',
                        required=False,
                        help='Name of the project (required if not in cfg file)')
    parser.add_argument('--Summary',
                        '-S',
                        required=False,
                        action="store_true",
                        help='set if only list of id , status,time wanted')
    parser.add_argument('--selectedField',
                        '-s',
                        required=False,
#                        action='append',
                        default=None,
                        help='Field name to append to selected fields list')
    parser.add_argument('--config-file','-C',metavar='FILE',help="read configuration from FILE: default:~/.geosmeta/geosmeta.cfg")
    args = parser.parse_args()
    query = args.query
    projectName = args.projectName
    flds=args.selectedField
    print("flds %s" %flds)
    gm = GeosMETA(configFilePath=args.config_file)
        # Submit the query
    try:
                adict=None
                if args.Summary:
                     adict={'summary':'T'}
                elif args.selectedField:
                     adict={'selectedFields':flds}

                resultJSON = gm.findActivities("A",projectName, query, adict)

                print((json.dumps(resultJSON,
                                indent=2,
                                sort_keys=True)))

                print("\n no. docs: %d\n"%(len(resultJSON['_items'])))
                for itm in resultJSON['_items']:
                   print(itm['_id'])

                try:
                   while ('next' in resultJSON['_links']):
                           mynext=resultJSON['_links']['next']['href']

                           print("retrieving %s\n"%(mynext))

                           resultJSON=gm.getHREF(mynext,projectName, selectedFields=flds)
                           print("\n no. docs: %d\n"%(len(resultJSON['_items'])))
                           for itm in resultJSON['_items']:
                              print(itm['_id'])
                           #print "resultJSON %s\n"%(resultJSON)

                           #sys.stdout.write(json.dumps(resultJSON,
                                            #indent=2,
                                            #sort_keys=True))
                except Exception as err:
                         sys.stderr.write('next page error %s\n' % str(err))
                sys.stderr.write('The end\n' )
                sys.exit(0)
    except Exception as err:
            sys.stderr.write('Error submitting the query:\n')
            sys.stderr.write('%s\n' % str(err))
            sys.exit(1)
    else:
            sys.stdout.write('Received activities:\n\n')
            sys.exit(0)


if __name__ == '__main__':
    main()
