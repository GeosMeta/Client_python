from geosmeta import GeosMETA
import argparse
import sys
# import json
import os
import copy
from gmTestBase import TestGeosMetaBase

class TestGeosMeta(TestGeosMetaBase):

  def checkActivity(self,actdoc,indict, supers=False):
      self.subTitle( "checkActivity for id %s"%actdoc)
             # retrieve the full document
      act1=self.gm.getDoc('A',None, actdoc)
      self.checkedDoc=act1 
      self.pulse( act1['_id'] ==  actdoc, 
           "failed to retrieve activity %s"%actdoc)


      self.check( "_callback_issues" not in act1, 
           "no callback issues")
#      import pdb; pdb.set_trace()
      if "_callback_issues"  in act1:
         print(" %s"%str(act1[ "_callback_issues" ]))

#      print (act1)
#      import pdb;pdb.set_trace()

      for ik in ['testing','hostname','cwd']:
            self.check( act1['gmdata'][ik]==indict[ik], "testing for keyword %s"%ik)
      if 'input_files' in indict:
         self.check( len(indict['input_files']) ==
                         len(act1['input_file_docs']),
                            "test number of input_files")
      if 'output_files' in indict:
         self.check( len(indict['output_files']) ==
                         len(act1['output_file_docs']) ,
                            "test number of output_files")
      self.check( act1['stati'][0]['status'] =='Current',
               "have stati[0] %s"%act1['stati'][0]['status'])
      self.check( act1['gmstatus']=='Current' ,
                    "gmstatus %s is Current"%act1['gmstatus'])

      if 'output_files' in indict:
         for (i,(fk,fd)) in enumerate(indict['output_files']):
            self.check( act1['output_file_docs'][i]['filename'] ==fk,
                      "file %d, %s is in output_file_docs" \
                      %(i,fk) )

      if 'input_files' in indict:
         for (i,fk) in enumerate(indict['input_files']):
            self.check( act1['input_file_docs'][i]['filename'] ==fk,
                      "file %d, %s is in input_file_docs" \
                      %(i,fk) )
           # check the gmfiles and links to/from the activity

      project_id=None

      print("        retrieving gmfiles to check against activity")

           # should drop output_files from the activity
#      for (fn,gmfile) in zip(act1['gmdata']['output_files'],
#                             act1['output_file_docs']):
#
#
      for fnl in act1['output_file_docs']:
           fn=fnl['filename']
           gmfile=fnl['file_id']

           try:
              gmfileRes=self.gm.getDoc('F',project_id, gmfile)
           except:
               import pdb;pdb.set_trace()
               
           self.check( gmfileRes['_id'] ==gmfile, 
               "retrieved output_file_doc with  _id %s "%(gmfile))
               # "retrieved gmfile _id %s is in %s"%(gmfile, str(gmfileRes)))

           self.check( gmfileRes['filename'] ==fn,"tested files %s %s"\
                       %(gmfileRes['filename'], fn))
           if 'made_by'in act1:
                self.check( gmfileRes['made_by'] ==act1['_id'],
                      "made_by is correct for %s"%fn)
           if supers:   # superseding previous version of file
                self.check( gmfileRes['version']==self.versions[fn]+1,
                           "version number got %d, expected %d"\
                           %(gmfileRes['version'],self.versions[fn]+1))
           self.versions[fn]=gmfileRes['version']

      if "input_file_docs" in act1:
         if len(act1["input_file_docs"]) > 0:
            for fnl in act1['input_file_docs']:
              fn=fnl['filename']
              gmfile=fnl['file_id']
                # consumer in list of gmfile?
                # what else?
              if gmfile: # can be none
                 gmfileIn=self.gm.getDoc('F',project_id, gmfile)          
                 self.check( gmfileIn['filename'] ==fn,
                       "retrieved input_file %s"%(fn))
                 self.check(act1['_id'] in  gmfileIn['consumers'],
                       "are flagging our activity as a consumer of %s"%fn)

  def test_activity1(self):
      '''
      write activity and correponding output file gmfiles
      Note, no input files used here.
      '''
	# check if have tests' docs in database
        # if so then change gmTestGlob 

		# not coded.

        # create an activity that makes 2 files
#      import pdb;pdb.set_trace()
      self.startTest( "test_activity1")
      self.adict=dict()
      self.adict['testing']=self.testFlag
      self.adict['hostname']=os.uname()[1]
      self.adict['cwd']=os.getcwd()
#      self.adict['input_files']=[]
      self.firstFile='1_1.%s'%self.testFlag  # save for later testing
      self.adict['output_files']=[[self.firstFile,{'md5sum':'1111'}],
                                  [ '1_2.%s'%self.testFlag, None]]


      try:
            project_id=None # it comes from the geosmeta.cfg file
            self.result1 = self.gm.addDoc(project_id,self.adict)
      except Exception as err:
            sys.stderr.write('Error creating gmDoc:\n')
            sys.stderr.write('%s\n' % str(err))
            sys.exit(1)
          # some structures for later validating test
      self.versions=dict()       

             # test returned json
      self.pulse('_status' in  self.result1,
                 "check added 1st activity %s"%str(self.result1) )
      self.check( self.result1['_status'] == 'OK', 
             "page inserted with result:\n  %s"%str(self.result1))
     
      self.activity1=self.result1['_id']

      self.checkActivity( self.activity1, self.adict)

                 ############

      self.subTitle("unknown input_file")

      self.cdict=copy.deepcopy(self.adict)
      notKnown=self.testFlag+'.datZASEDFGHJK'
      self.cdict['input_files']=[notKnown] # reset to a list and recheck
                                     # note - this file does not exist
      self.cdict['output_files']=[[self.firstFile+"2",None], ['1_2.%s_2'%self.testFlag,None]]

      try:
            project_id=None # it comes from the geosmeta.cfg file
            self.result1c = self.gm.addDoc(project_id,self.cdict)
      except Exception as err:
            sys.stderr.write('Error creating gmDoc:\n')
            sys.stderr.write('%s\n' % str(err))
            sys.exit(1)
             # test returned json
      self.pulse('_status' in  self.result1c,
                 "check added activity with unknown file %s"%str(self.result1c) )
      # check got extra field for this missing input
      self.check( self.result1c['_status'] == 'OK', 
             "pagewith unknown file  inserted :\n  %s"%str(self.result1c))
     
      self.activity1c=self.result1c['_id']

      self.checkActivity( self.activity1c, self.cdict)
      self.check( self.checkedDoc['input_file_docs'][0]['filename']==notKnown,"added unknown file")
      self.check( self.checkedDoc['input_file_docs'][0]['file_id']==None,
                                     "added unknown file so it has no  gmfile")
      self.check( self.checkedDoc['unknown_input_files'][0]==notKnown,"recognised unknown file")
                 # notign the issue here is to allow the user to recognise this condition
                 # but not enforce the need to have a source activ ity for each input file.
      if self.verbose:
         print (self.checkedDoc)
      self.endTest("end of test_actvity1")
      return

  def step2(self, superseding):
        # superseding is true it this is a 2nd call of this test.
	# set up another dictionary - just copy what we have then reset
        # inputs as the outputs from teh previous document,

      bdict=copy.deepcopy(self.adict)
      bdict['input_files']=[] 
      for oplin in bdict['output_files']:
          bdict['input_files'].append(oplin[0])
      bdict['output_files']=[['2_1.%s'%self.testFlag, None]]
      try:
            project_id=None # it comes from the geosmeta.cfg file
            import pdb;pdb.set_trace()
            bres = self.gm.addDoc(project_id,bdict)
      except Exception as err:
            sys.stderr.write('Error creating gmDoc:\n')
            sys.stderr.write('%s\n' % str(err))
      if not superseding:
         # creatign 2n#d activity for 1st time 

         self.activity2=bres['_id']

         self.checkActivity( self.activity2, bdict,supers=False)
      else:
              # repeated step to test version numbers in gmfiles
              # and superseding flags in activities.
         self.activity2repeat=bres['_id']

         self.checkActivity( self.activity2repeat,bdict, supers=True)


  def step3(self, superseding):
      bdict=copy.deepcopy(self.adict)
      bdict['input_files']=['2_1.%s'%self.testFlag]
      bdict['output_files']=[['3_1.%s'%self.testFlag,None]]
      try:
            project_id=None # it comes from the geosmeta.cfg file
#            import pdb;pdb.set_trace()
            bres = self.gm.addDoc(project_id,bdict)
      except Exception as err:
            sys.stderr.write('Error creating gmDoc:\n')
            sys.stderr.write('%s\n' % str(err))
      if not superseding:
         # creatign 2nd activity for 1st time 

         self.activity3=bres['_id']

         self.checkActivity( self.activity3, bdict,supers=False)
      else:
              # repeated step to test version numbers in gmfiles
              # and superseding flags in activities.
         self.activity3repeat=bres['_id']

         self.checkActivity( self.activity3repeat,bdict, supers=True)


  def test_inputFiles(self):
      ''' use both outputs from act1 
      '''
      self.startTest("test_inputFiles")
      self.step2(False) 
		# step 2, file 1
      self.subTitle("repeating step 2")
      self.step2(True)  # repeating step 2 to check superceding flags.

      self.endTest("end of test_inputFiles")
      return

  def test_activity3(self):
      ''' chain a 3rd activity to let downstream tests run
      '''
      self.startTest("test_activity3")
      self.step3(False) 
		# step 2, file 1
      self.subTitle("repeating step 3")
      self.step3(True)

      self.endTest("end of test_activity3")
      return
  def test_findFileUse(self):
      ''' can we retrieve list of activities that usei or create a named file?
          And manage a request for a file that does not exist?
      '''

      self.startTest("test_findFileUse")
      self.subTitle("test if can find creating activity for a named file")
      (ndocs,currentlist) = self.gm.findFileUse(None,'2_1.%s'%self.testFlag,"output_file_docs")
      self.check(ndocs==2,"should have ndocs=2, have %d"%ndocs)
      self.check(len(currentlist)==1,"should have one current id listed")
      self.check( self.activity2repeat==currentlist[0],
                "test found the current second activity" )

      self.subTitle("look for creator of a nonexisting file")
      (ndocs,idlist) = self.gm.findFileUse(None,'NOSUCHFILE.XXXXXXXXX',
                                     "output_file_docs")
      self.check(ndocs==0,"should have found no docs got %d"%ndocs)

              # code for input_files test.
              # note currently limited to 25 ids - see api.py
      self.endTest("end of test_findFileUse")
      return

  def test_validationError(self):
      ''' force a validation erorr, due to the settings.py definitions
      being broken
      Get the error, then fix it and see all is working.
      '''
#      import pdb; pdb.set_trace()
      self.startTest("test_validationError")
      bdict={'afield':1}
      bdict['testing']=self.testFlag

      self.subTitle("break rules in setting.py")
           # use a dict not a list.

      bdict['input_files']={'a':1,'b':2}  # any nonsense will do to break validation
      try: 
            resultV = self.gm.addDoc(None, bdict)
            self.check(False,"should have triggered event handler")
      except Exception as err:
            self.check(str(err).startswith('Status code: 422') and 
               str(err).find(
        '"input_files": "must be of list type"'),
                 "reporting input_files should be a list  %s"%str(err)) 

      self.endTest("end of test_validation")

  def test_errorPropagation(self):
      ''' set 2nd activity to error
          should cahnge the current instance of activity 2 (not supeceded one)
          and the 3rd activity (current one also)
          Changes being to stati and gmstatus fields
      '''
      self.startTest("test_errorPropagation")

      
      self.endTest("not coded end of test_errorPropagation")
       
def runTests1():
   
      # in general, the order matters as docs are created
      # and for example activity states etc change
      # during the tests.

   parser = argparse.ArgumentParser(
             description="integration tests  1 - activity and gmfile documents")
   parser.add_argument('flag',help='flags this instance of the tests')
   #parser.add_argument('--flag',
#                        '-f',
#                        required=True,
#                        help='flags this instance of the tests')

   parser.add_argument('--stopafter','-s', 
                       required=False, 
                       type=int,
                       help='run these first s tests only')

   parser.add_argument('--verbose','-v', 
                       required=False, 
                       default=False, action="store_true",
                       help='more verbose output')

   args = parser.parse_args()

   gt=TestGeosMeta()

   gt.testFlag=args.flag
   gt.verbose=args.verbose
   gt.gm = GeosMETA()
   testList=['test_validationError',
              'test_activity1', 'test_inputFiles','test_activity3',
              'test_findFileUse','test_validationError',
              'test_errorPropagation','test_errorPropagation']

   ntests=len(testList)
   if args.stopafter:
        ntests=args.stopafter

   for itest in range (0,ntests):

      getattr(gt,testList[itest])()

   sys.exit()
if __name__ == '__main__':
   runTests1()
