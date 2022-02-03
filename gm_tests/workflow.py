#!/usr/bin/env python
#
# Copyright (c) The University of Edinburgh, 2014.
#
from geosmeta import GeosMETA
import argparse
import sys
import json
import os
project=None

def docErr(activityID, newStatus,  message, goDownStream,sproject=None,configFile=None ):

    gm = GeosMETA(configFilePath=configFile)

        #first get the document and then extract the etag
    try:
            resultJSON = gm.getActivity(project, activityID)
    except Exception as err:
            sys.stderr.write('Error retrieving the etag:\n')
            sys.stderr.write('%s\n' % str(err))
            sys.exit(1)
    else:
            sys.stdout.write('Etag retrieved successfully: \n')
            activityID = resultJSON['_id']
            activityEtag = resultJSON['_etag']
            print ('Etag: ' + activityEtag)
            print ('_id:' + activityID)


        # Now update the activity using its _id, _etag and the change to be made.
    try:
            result = gm.updateDocStatus(activityID, activityEtag,
                                        newStatus,message, goDownStream)
            print(result)
    except Exception as err:
            sys.stderr.write('Error setting error status:\n')
            sys.stderr.write('%s\n' % str(err))
            sys.exit(1)

    



def addTheDoc(metaFields,sproject=None,configFile=None ):

    gm = GeosMETA(configFilePath=configFile)
    try:
            result = gm.addDoc(project,metaFields)
    except Exception as err:
            sys.stderr.write('Error creating activity:\n')
            sys.stderr.write('%s\n' % str(err))

    else:
        sys.stdout.write('gmdoc  was created successfully\n')
#        sys.stdout.write(json.dumps(result,
                                            #indent=2,
                                            #sort_keys=True) )
        sys.stdout.write('\n returning successfully\n')
        return result


def test1(tname):

    adict=dict()
    adict['trial']=1
    adict['hostname']=os.environ["HOSTNAME"]
    adict['cwd']=os.getcwd()

    adict['testname']=tname
    adict['input_files']=["unknown"+tname]
    adict['output_files']=[["1."+tname,None], ["2."+tname,None]]
    adict['tname']=tname
    adict['gmname']="activity_1"
    resA=  addTheDoc(adict)
    print(resA['_id'])

    adict['input_files']=["1."+tname]
    adict['trial']=2
    adict['gmname']="activty_2"
    adict['output_files']=[["3."+tname, {'a':adict['cwd']}],[ "4."+tname,None]]
    resB=  addTheDoc(adict)
    print(resB['_id'])

    adict['input_files']=["2."+tname, "4."+tname]
    adict['trial']=3
    adict['gmname']="activty_3"
    adict['output_files']=[["5."+tname,None]]

    resC =   addTheDoc(adict)
    print(resC['_id'])

    adict['input_files']=["2."+tname, "4."+tname]
    adict['trial']=4
    adict['gmname']="activty_4"
    adict['output_files']=[["6."+tname,None]]

    resD =   addTheDoc(adict)
    print(resD['_id'])


def test2(tname):
# adict contains metadata fileds inserted into each of several gmDocs
# the keyword trial is hte only distinguishign feature, other than different
# input and output files.
# In real use, these different docs would be from different scripts.


    adict=dict()
    adict['trial']=1
    adict['hostname']=os.environ["HOSTNAME"]
    adict['cwd']=os.getcwd()

    adict['testname']=tname
    adict['output_files']=[["1."+tname,None],[ "2."+tname,None]]
    adict['tname']=tname
    adict['gmname']="activity_1p2"
    res=  addTheDoc(adict)
    print(res['_id'])

    adict['input_files']=["1."+tname]
    adict['trial']=2
    adict['output_files']=[["3."+tname,None],[ "4."+tname,None]]
    adict['gmname']="activity_2p2"
    res=  addTheDoc(adict)
    print(res['_id'])

    adict['input_files']=["2."+tname]
    adict['trial']=3
    adict['output_files']=[["6."+tname,{"6meta":6}],[ "5."+tname,None]]
    adict['gmname']="activity_3p2"

    res =   addTheDoc(adict)
    print(res['_id'])

    adict['input_files']=["5."+tname, "4."+tname]
    adict['trial']=4
    adict['output_files']=[["7."+tname,None]]
    adict['gmname']="activity_4p2"

    res =   addTheDoc(adict)
    print(res['_id'])

    adict['input_files']=["7."+tname]
    adict['trial']=5
    adict['gmname']="activity_5p2"
    adict['output_files']=[["8."+tname,None]]

    res =   addTheDoc(adict)
    print(res['_id'])

def test3(tname):
        # create new filr 5.tname, 
        # with new activity, superceing old one.
        # does mean hav have two square nodes for versions of the file.

    adict=dict()
    adict['input_files']=["3."+tname, "8."+tname]
    adict['trial']=4
    adict['output_files']=[["5."+tname,{'a':5}]]
    adict['gmname']=tname+"_recurse"
    res  =   addTheDoc(adict)
    print(res['_id'])
def test_xtom(tname):
        # create new filr 5.tname, 
        # with new activity, superceing old one.
        # does mean hav have two square nodes for versions of the file.

    adict=dict()
    adict['input_files']=["sample_"+tname]
    adict['gmname']="xtomExpt"
    adict['output_files']=[["a_"+tname+".dat",{'a':'a'}],["b_"+tname+".dat",None]]
    adict['gmname']=tname+"_expt"
    res  =   addTheDoc(adict)
    print(adict,"\n",res['_id'])

    adict['input_files']=["a_"+tname+".dat","b_"+tname+".dat"]
    adict['gmname']="prog1"
    adict['output_files']=[["c_"+tname+".dat",None]]
    res  =   addTheDoc(adict)
    print(adict,"\n",res['_id'])

    adict['input_files']=["a_"+tname+".dat","b_"+tname+".dat"]
    adict['gmname']="prog2"
    adict['output_files']=[["d_"+tname+".dat",None]]
    ares  =   addTheDoc(adict)
    print(adict,"\n",ares['_id'])
    print (ares)
    activityID=ares['_id']

    bdict={}
    bdict['input_files']=["c_"+tname+".dat","d_"+tname+".dat"]
    bdict['gmname']="prog3"
    bdict['output_files']=[["end_"+tname+".dat",None]]
    res  =   addTheDoc(bdict)
    print(bdict,"\n",res['_id'])

    message="found error"
    newStatus="E"
    goDownStream=True
    result=docErr(activityID, newStatus,message, goDownStream)

if __name__ == '__main__':

    tname=sys.argv[1]
    if sys.argv[2]=="1":
       test1(tname)
    elif sys.argv[2]=="2":
       test2(tname)
    elif sys.argv[2]=="3":
       test3(tname)
    elif sys.argv[2]=="xtom":
       test_xtom(tname)


