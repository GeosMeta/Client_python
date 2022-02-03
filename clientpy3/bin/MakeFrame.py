import wx
class MyFrame(wx.Frame):
    def __init__(self, parent, id, title,text):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition,
wx.Size(325, 320))

        self.title=title
        self.text=text
       # panel = wx.Panel(self, -1)

       # font2 = wx.Font(10, wx.ROMAN, wx.NORMAL, wx.NORMAL)

        box= wx.TextCtrl(self, pos=(300,20), size=(200,300), style=wx.TE_MULTILINE |
wx.TE_READONLY)
        box.AppendText(text)
        #lyrics2 = wx.StaticText(panel, -1, text,(30,100))
#        lyrics2 = wx.StaticText(panel, -1, text,(30,100), style=wx.ALIGN_CENTRE)
        #lyrics2.SetFont(font2)
        #self.Center()
