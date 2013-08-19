#!/usr/bin/env python
# gauge.py
# Updated to follow style guidelines

import wx


class MyFrame(wx.Frame):
    def __init__(self, parent, ID, title):
        wx.Frame.__init__(self, parent, ID, title)

        self.timer = wx.Timer(self, 1)
        self.count = 0

        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)

        panel = wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
	#self.slider = wxSlider(panel,
        self.gauge = wx.Gauge(panel, -1, 50, size=(250, 25))
        self.btn1 = wx.Button(panel, wx.ID_OK)
        self.btn2 = wx.Button(panel, wx.ID_STOP)
        self.text = wx.StaticText(panel, -1, "Task to be done")

        self.Bind(wx.EVT_BUTTON, self.OnOk, self.btn1)
        self.Bind(wx.EVT_BUTTON, self.OnStop, self.btn2)

        hbox1.Add(self.gauge, 1, wx.ALIGN_CENTRE)
        hbox2.Add(self.btn1, 1, wx.RIGHT, 10)
        hbox2.Add(self.btn2, 1)
	#hbox1.Add(self.text, 1)        
	#hbox3.Add(self.text, 1)
        vbox.Add((0, 50), 0)
        vbox.Add(hbox1, 0, wx.ALIGN_CENTRE)
        vbox.Add(self.text, 1, wx.ALIGN_CENTRE)
        vbox.Add(hbox2, 1, wx.ALIGN_CENTRE)
        vbox.Add(hbox3, 1, wx.ALIGN_CENTRE)

        panel.SetSizer(vbox)
        self.Centre()

    def OnOk(self, event):
        if self.count >= 50:
            return
        self.timer.Start(150)
        self.text.SetLabel("Task in Progress")
	self.btn2.SetLabel("Stop")

    def OnStop(self, event):
	
	if not self.timer.IsRunning():
	    self.count = 0
	    self.gauge.SetValue(self.count)
	    self.btn2.SetLabel("Stop")
	    self.text.SetLabel("Task to be Done")

        if self.count == 0 or self.count >= 50 or not self.timer.IsRunning():
            return
	
        self.timer.Stop()
        self.text.SetLabel("Task Interrupted")
	self.btn2.SetLabel("Reset?")
        wx.Bell()

    def OnTimer(self, event):
        self.count = self.count +1
        self.gauge.SetValue(self.count)
	self.text.SetLabel(str(self.count))
        if self.count == 50:
            self.timer.Stop()
            self.text.SetLabel("Task Completed")
	    self.btn2.SetLabel("Reset?")

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, "gauge.py")
        frame.Show(True)
        return True


app = MyApp(0)
app.MainLoop()
