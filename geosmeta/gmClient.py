__all__ = ['GMClient','gmArgumentParser']

import json
import sys
import hashlib
import zlib
import base64
import getpass,socket
import time
import argparse
import os
from .api import GeosMETA

# create a standard argument parser
defaultCfgFile='~/.geosmeta/geosmeta.cfg'
gmArgumentParser = argparse.ArgumentParser(add_help=False)
group = gmArgumentParser.add_argument_group('GeosMeta Options')
group.add_argument('--config-file',
                   '-C',
                   metavar='CFG',
                   default=defaultCfgFile,
                   help="read configuration from CFG: default: %s"%defaultCfgFile)
group.add_argument('--project',
                   '-p',
                   help='Name of the project (can be in cfg file)')
group.add_argument('--gm-verbose', action="store_true", default=False, help="gm verbosity")

def hashfile(aname,blocksize=65536):
    hash = hashlib.md5()
    with open(aname,"rb") as afile:
        for chunk in iter(lambda: afile.read(blocksize), b""):
            hash.update(chunk)
    return hash.hexdigest()

def compressFile(aname,blocksize=65536):
    with open(aname,"rb") as afile:
        hash = hashlib.md5()
        cmprs = zlib.compressobj()
        cstring = ""
        for chunk in iter(lambda: afile.read(blocksize), b""):
            hash.update(chunk)
            cstring += cmprs.compress(chunk)
        cstring += cmprs.flush()
        return hash.hexdigest(),base64.b64encode(cstring)

class GMClientBase(object):
    protectedKeys = ['input_files','output_files','ImportedURIs','script',
                     'user','hostname','start','end']
    def __init__(self):
        self._inputs = []
        self._outputs = []
        self._importedURIs = []
        self._params = {}

        # setup standard meta data
        self.start()
        self._params['user'] = getpass.getuser()
        self._params['hostname'] = socket.gethostname()
        # get os

    def start(self):
        self._params['start'] = time.time()

    def end(self):
        self._params['end'] = time.time()

    def addInput(self,input):
        if input not in self._inputs:
            self._inputs.append(input)

    def addInputList(self,inlist):
        for input in inlist:
            self.addInput(input)
    
    def addOutput(self,output):
        if output not in self._outputs:
            self._outputs.append(output)

    def addOutputList(self,outlist):
        for output in outlist:
            self.addOutput(output)

    def addParam(self,key,val):
        if key in self.protectedKeys:
            raise KeyError('%s is a protected key'%key)
        self._params[key] = val

    def addParamDict(self,pdict):
        for k in pdict:
            self.addParam(k,pdict[k])

    def addScript(self,fname=None):
        if fname==None:
            fname = os.path.abspath(sys.argv[0])
        md5,cmprs = compressFile(fname)
        self._params['script'] = {
            'name' : fname,
            'md5' : md5,
            'content' : cmprs}

    def genDoc(self,checkFiles=True):
        
        # check that input, output and external files are also mentioned in the params dictionary
        if checkFiles:        
            for a in [self._inputs,self._outputs,self._importedURIs]:
                for f in a:
                    if f not in list(self._params.values()):
                        raise LookupError('file %s not in params'%f)

        if 'end' not in self._params:
            self.end()
            
        return dict(list(self._params.items()) +
                               [('input_files',self._inputs)] +
                               [('output_files',self._outputs)] +
                               [('ImportedURIs',self._importedURIs)])

    def genJason(self,checkFiles=True):

        return json.dumps(self.genDoc(checkFiles=checkFiles))

class GMClient(GMClientBase):
    def __init__(self,gmArgs):
        GMClientBase.__init__(self)

        self.proj=gmArgs.project
        self.gmverbose=gmArgs.gm_verbose
        self.gm = GeosMETA(gmArgs.config_file) #,gmArgs.project)
        
    def close(self,checkFiles=True):
        doc = self.genDoc(checkFiles)
        reply=self.gm.addDoc(self.proj,doc)
        if self.gmverbose:
            print("get id")
            print(reply)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(parents=[gmArgumentParser])
    args = parser.parse_args()

    gm = GMClient(args)  #Base()
    gm.addOutput('inA')
    gm.addOutput('inB')
    gm.addParam('paramA',10)
    gm.addParamDict({'paramB':20,'paramC':'golf'})
    gm.addScript()
    gm.close(False)

    gn = GMClient(args)
    gn.addInput('inA')
    gn.addInput('inB')
    gn.addOutput('outA')
    gn.addParam('paramA',102)
    gn.addParamDict({'paramB':202,'paramC':'lotto'})
    gn.addScript()
    gn.close(False)

#    print gm.genJason(checkFiles=False)
