#!/bin/env python
import argparse
import geosmeta

if __name__ == '__main__':

    
    parser = argparse.ArgumentParser(description='try out geosmeta client', parents = [geosmeta.gmArgumentParser])
    parser.add_argument('inputs',metavar='INPUT',nargs='+',help='input files')
    parser.add_argument('output',metavar='OUTPUT',help='output file')
    parser.add_argument('--arg-a','-a',metavar='A',type=int,help='paramater A')
    parser.add_argument('--arg-b','-b',metavar='B',type=float,help='paramater B')
    args = parser.parse_args()

    gm = geosmeta.GMClient(args)
    gm.addInputList(args.inputs)
    gm.addOutput(args.output)
    gm.addParamDict(vars(args))
    gm.addScript()

        # do script work here
        # might check results

        # add other parameters - hidden output files, parameters set in config files...

    #print gm.genJason(checkFiles=False)
    gm.close(checkFiles=False)
