import wx
import wx.html
import controller
import controller.sample

class FetchSamplePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)
        self.parent = parent
        self.sample_id = wx.TextCtrl(self, wx.ID_ANY, "000001A")
        self.fetch_btn = wx.Button(self, wx.ID_ANY, "Fetch data")
        self.Bind(wx.EVT_BUTTON, self.on_fetch, self.fetch_btn)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.sample_id, 0, wx.ALL, 10)
        sizer.Add(self.fetch_btn, 0, wx.ALL, 10)
        self.SetSizer(sizer)
    def on_fetch(self, event):
        self.parent.fetch_sample(self.sample_id.GetLabel())
        event.Skip()
#----------------------------------------------------------------------
class SampleInfoPanel(wx.Panel):
    def __init__(self, parent, sample=None):
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)
        sizer = wx.GridSizer(2, 5, 5)
        sizer.Add(wx.StaticText(self, wx.ID_ANY, "Sample taken"),
                  1, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(wx.StaticText(self, wx.ID_ANY, "Genotyping"),
                  2, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(wx.StaticText(self, wx.ID_ANY, "Variant calling"),
                  2, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(wx.StaticText(self, wx.ID_ANY, "QC status"),
                  1, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(wx.StaticText(self, wx.ID_ANY, "View raw"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        if sample:
            sizer.Add(wx.TextCtrl(self, wx.ID_ANY, str(sample["sample_taken"]),
                                  style=wx.NO_BORDER), 1, wx.EXPAND)
            sizer.Add(wx.TextCtrl(self, wx.ID_ANY, sample["genotyping"],
                                  style=wx.NO_BORDER), 2, wx.EXPAND)
            sizer.Add(wx.TextCtrl(self, wx.ID_ANY, sample["variant_calling"],
                                  style=wx.NO_BORDER), 2, wx.EXPAND)
            sizer.Add(wx.TextCtrl(self, wx.ID_ANY, sample["qc_status"],
                                  style=wx.NO_BORDER), 1, wx.EXPAND)
            sizer.Add(wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap("igv.bmp")))
        self.SetSizer(sizer)
        

#----------------------------------------------------------------------       
class SamplePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.sample_id = ""
        self.sample = None 
        self.fetch_sample_panel = FetchSamplePanel(self)
        self.SetBackgroundColour('#efefef')
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.fetch_sample_panel, 0, wx.EXPAND)
        self.SetSizer(self.sizer)
           
    def fetch_sample(self, sample_id):
        self.sample_id = sample_id
        self.sample = controller.sample.get_sample_record(sample_id)
        if not self.sample:
            self.not_found()
        else:
            self.parent.Hide()
            self.show_sample()
            main_frame = self.GetTopLevelParent()
            main_frame.show_all()
            self.parent.Show()

    def show_sample(self):
        h1 = wx.StaticText(self, wx.ID_ANY, "Sample info")
        h2 = wx.StaticText(self, wx.ID_ANY, "QC report")
        h3 = wx.StaticText(self, wx.ID_ANY, "Coverage")
        h1.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        h2.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        h3.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.sample_info_panel = SampleInfoPanel(self, self.sample)
        self.qc_report = wx.html.HtmlWindow(self, wx.ID_ANY,
                                            style=wx.SUNKEN_BORDER)
        self.qc_report.LoadPage(self.sample["qc_report"])
        self.coverage = wx.html.HtmlWindow(self, wx.ID_ANY,
                                           style=wx.SUNKEN_BORDER)
        self.coverage.LoadPage(self.sample["coverage"])
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.fetch_sample_panel, 0, wx.EXPAND)
        self.sizer.Add(h1, 0, wx.ALL, 10)
        self.sizer.Add(self.sample_info_panel, 0, wx.EXPAND)
        self.sizer.Add(h2, 0, wx.ALL, 10)
        self.sizer.Add(self.qc_report, 1, wx.EXPAND)
        self.sizer.Add(h3, 0, wx.ALL, 10)
        self.sizer.Add(self.coverage, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Layout()
       
    def not_found(self):
        dlg = wx.MessageDialog(self, "Not found", "Sample", wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()



#----------------------------------------------------------------------
class MainFrame(wx.Frame):
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="genAP wb", size=(1024, 800))
        sample_panel = SamplePanel(self)
        
        self.Show()
        
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
