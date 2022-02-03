

class TestGeosMetaBase(object):

  def __init__(self):
      self.error=False

  def startTest(self,msg):
      print("***********************************************")
      print("**** Start of "+ msg)
      return

  def subTitle(self,msg):
      print("-----------------------------------------------")
      print("**** Subtest: "+ msg)
      return

  def abandon(self,msg):
      print("fatal error")
      print(msg)
      print("entering debugger -  quit() to exit")
      import pdb; pdb.set_trace()

  def pulse (self,test,msg):
      if not test:
         self.abandon("failed pulse test: " +msg)

  def check (self,test,msg):
      if not test:
         self.error=True
         print("\n.....failed - %s"%msg)
      else:
         print("...... passed - %s "%msg)

  def endTest(self,msg):
      print(msg)
      if self.error:
         self.abandon("found error(s) - stopping testing")

