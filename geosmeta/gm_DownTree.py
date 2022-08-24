#!/usr/bin/env python
#
# Copyright (c) The University of Edinburgh, 2015.
#
import sys
from .api import GeosMETA
import argparse
import json
import copy
import matplotlib.pyplot as plt
import networkx as nx
import wx

from matplotlib.backends.backend_wxagg import \
FigureCanvasWxAgg as FigCanvas, \
NavigationToolbar2WxAgg as NavigationToolbar

from . import AnnotateFinder 
from . import MakeFrame

class  afWithPop(AnnotateFinder.AnnoteFinder):
    def __init__(self, xdata, ydata, annotes,nodeHasID, gm, axis=None,
xtol=None, ytol=None):
        self.nodeHasID= nodeHasID
        self.gm= gm
#        print "ann init"
        #print zip(self.nodeHasID,annotes)
        AnnotateFinder.AnnoteFinder.__init__(self, xdata, ydata, annotes, axis=None,
xtol=None, ytol=None)
#        for i,k in enumerate(zip(self.nodeHasID,self.data)):
           #print i,k
        #print "leave init of adWithPop"

    def __call__(self, event):
#        print "call"
        AnnotateFinder.AnnoteFinder.__call__(self, event)
#        for i,k in enumerate(zip(self.nodeHasID,self.data)):
           #print i,k
        #print self.hitIndex
        if len(self.hitIndex)>0:
            myhit=self.hitIndex[0]
            self.hitIndex=[]
            #print self.data[myhit], self.nodeHasID[myhit]
            if self.nodeHasID[myhit]:
                # gm = GeosMETA()
                 id=self.data[myhit][2]
                 resultJSON = self.gm.getActivity(None, id)
                 outtxt=json.dumps(resultJSON, 
                                indent=2,
                                sort_keys=True)
                 self.nuFrame=MakeFrame.MyFrame(None, -1,self.data[myhit][2],outtxt)
                 self.nuFrame.Show(True)

OUT_COL='yellow'
IN_COL='b'
class gmTreeNetworkFrame(wx.Frame):

    def __init__(self,gm):
        wx.Frame.__init__(self, None, -1)
        self.panel = wx.Panel(self)
        self.fig = plt.figure()
        self.canvas = FigCanvas(self.panel, -1, self.fig)
        self.G=nx.MultiDiGraph() # gives direction to edges

        self.nodename=[]
        self.nodeHasId=[] # "activity","file",?
        self.nodeColour=[] 
        self.edgeColour=[] 
        self.statusColour={'Current':'g','Error':'r','DownStreamOfError':'orange'}
        self.docIndex=[]
        self.fileIndex=[]
        self.docCol=[]
        self.fileCol=[]
        self.gm=gm

    def plotGraph(self):
        
#        pos= nx.drawing.graphviz_layout(self.G)
        pos=nx.spring_layout(self.G)
#        pos=nx.graphviz_layout(self.G,prog='dot')
        #print "pos"
        #print pos
        annotes=[]
        x=[]
        y=[]
        for key in self.nodename: # not pos:
            d=pos[key]
            annotes.append(str(key))
            x.append(d[0])
            y.append(d[1])

        nx.draw_networkx_nodes(self.G,pos,node_size=1000,nodelist=self.docIndex,node_color=self.docCol)#'g')
        nx.draw_networkx_nodes(self.G,pos,node_size=100,nodelist=self.fileIndex,node_color=self.fileCol,node_shape='s')#'b')

        #print "drawing edges"
        #for (i,k) in enumerate( zip(self.G.edges(),self.edgeColour)):
           #print i,k
        
        nx.draw_networkx_edges(self.G,pos,alpha=0.5,width=2)# following fail: ,arrows=True,edge_color=self.edgeColour)

#        nx.draw_networkx_edges(self.G,pos,width=2,arrows=True)
        
        plt.axis('off')
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.toolbar = NavigationToolbar(self.canvas)
        self.vbox.Add(self.toolbar, 0, wx.EXPAND)
        self.panel.SetSizer(self.vbox)
        self.vbox.Fit(self)

        af=  afWithPop(x,y, annotes, self.nodeHasId, self.gm)
        self.canvas.mpl_connect('button_press_event', af)



    def whatColour(self,stat):
           col='b'
           if stat in self.statusColour:
               col=self.statusColour[stat]
           return col

    def graphOfGMidilist(self,infile,docids):
       for id in docids:
          # see if already done this node
          if self.G.has_node(id):
                   # just connect files to the node
              self.G.add_edge(infile,id)
              self.edgeColour.append(IN_COL)
          else:
                   # get doc for the activity

              aDoc = gm.getActivity(projectName, id)
              print(("recurse for %s with input %s\n"%(id,infile)))
          
              self.graphOfGMdoc(aDoc,linkFrom=infile)
 
    def graphOfGMdoc(self,aDoc,linkFrom=None):
       try:
            myid=aDoc['_id']
            self.nodename.append(myid)
            print("get status")
            mys = aDoc['gmstatus']
            print(mys)
            colStatus=self.whatColour(mys)
            self.nodeColour.append(colStatus)
            self.docCol.append(colStatus)
            self.nodeHasId.append(True)
            self.G.add_node(myid)
          #  self.docIndex.append(len(self.nodename)-1)
            self.docIndex.append(myid) #len(self.nodename)-1)

            if linkFrom:
                self.edgeColour.append(IN_COL)
                self.G.add_edge(linkFrom, myid)
            nextNodes= copy.deepcopy(aDoc["_gmTreeDown"])
            aDoc=None # this and deepcopy... 
                      #do they help memory management as poised to recurse?
            for outfile,outids in nextNodes:
                # might have met this node by another route, so check
                # and only use.... er... no... each file made in one place.
                #if not self.G.has_node(outfile):
                self.nodename.append(outfile)
                self.nodeColour.append(colStatus)
                self.fileCol.append(colStatus)
                self.nodeHasId.append(False)
                self.G.add_node(outfile)
                self.fileIndex.append(outfile) 
                self.G.add_edge(myid,outfile)
                self.edgeColour.append(OUT_COL)

            print("edges")
            ge=self.G.edges()
            print((len(ge)))
           # print len(self.edgeColour)
            for (i,k) in enumerate( zip(ge,self.edgeColour)):
                 print((i,k))
            if len(ge) != len(self.edgeColour) :
               print("mismatched lengths!")
               print(ge)
               print((self.edgeColour))
               print(myid)
               print(linkFrom)
               print(nextNodes)
           # print "nodes"
           # for (i,k) in enumerate( zip(self.nodeHasId, self.nodename)):
           #      print i,k
           # print "docindex"
           # print self.docIndex
           # print "fileindex"
           # print (self.fileIndex, self.fileCol)
                    
# call recursively here:

            for outfile,outids in nextNodes:
                self.graphOfGMidilist(outfile,outids)

       except Exception as err:
            sys.stderr.write('%s\n' % str(err))
            sys.stderr.write('Error adding %s to graph data structures:\n'%(aDoc['_id']))
            sys.exit(1) # beware continuing if lists might not be in sync.


def main():

         # Get command line arguments
    parser = argparse.ArgumentParser(description=\
                      """Display docs downstream of a query
     '"$and":[{"gmdata.input_files":{"$exists":false}},{"gmdata.trial":{"$exists":true}},{"gmdata.tname":
"MTNA "}]' """ )
    
    parser.add_argument('--query',
                        '-q',
                        required=True,
                     
                        help='key-value search query (required)')
    parser.add_argument('--projectName',
                        '-p',
                        required=False,
                        help='Name of the project (required if not in cfg file)')
    parser.add_argument('--config-file','-C',metavar='FILE',
                  help="read configuration from FILE: default:~/.geosmeta/geosmeta.cfg")
    args = parser.parse_args()
    query = args.query
    projectName = args.projectName

    app = wx.PySimpleApp()
    gm = GeosMETA(configFilePath=args.config_file)

    app.frame = gmTreeNetworkFrame(gm)

    
        # Submit the query
    try:
           resultJSON = gm.findActivities("A",projectName, query,None)

           for itm in resultJSON['_items']:
       #            print "need check if no input files?"
                   app.frame.graphOfGMdoc( itm)
           try:
               mayHaveNext=True
               while (mayHaveNext):
                   mynext=resultJSON['_links']['next']['href']

                   resultJSON=gm.getHREF(mynext)
                   for itm in resultJSON['_items']:
       #                   print "need check if no input files?"
                          graphOfGMdoc( itm['_id'])

                   print(("retrieved %s\n"%(mynext)))
                   #sys.stdout.write(json.dumps(resultJSON,
                                            #indent=2,
                                            #sort_keys=True))
                        # this does end in an err
           except Exception as err:
                        sys.stderr.write('end of scan \n')
                        app.frame.plotGraph()
    
                        app.frame.Show()
                        app.MainLoop()
    except Exception as err:
            sys.stderr.write('Error submitting the query:\n')
            sys.stderr.write('%s\n' % str(err))
            sys.exit(1)

        
if __name__ == '__main__':
    main()
