import wx
import controller.references

cols = [("gene", "Gene", 1),
        ("variant", "Variant (HGVS)", 1),
        ("source", "Source", 1),
        ("references", "Reference(s)", 2),
        ("previous_evaluations", "Previous evaluations?", 3),
        ("high_quality_evidence", "High quality evidence?", 2)]

#----------------------------------------------------------------------
class RefPanel(wx.Panel):
    def __init__(self, parent, refs):
        wx.Panel.__init__(self, parent, style=wx.BORDER_SUNKEN)
        self.refs = refs
        vs = wx.BoxSizer(wx.VERTICAL)
        hs = wx.BoxSizer(wx.HORIZONTAL)
        for col in cols: # add headers first
            hs.Add(wx.StaticText(self, wx.ID_ANY, col[1]), col[2], wx.EXPAND)
        hs.Add(wx.CheckBox(self, wx.ID_ANY, "Hide completed"), 1)
        vs.Add(hs, 0, wx.EXPAND|wx.TOP, 20)
        i = 0
        for ref in refs: # add row
            hs = wx.BoxSizer(wx.HORIZONTAL)
            for col in cols: # add row values
                c = wx.StaticText(self, wx.ID_ANY, ref[col[0]], name=str(i))
                c.SetBackgroundColour(wx.WHITE)
                hs.Add(c, col[2], wx.EXPAND|wx.TOP, 1)
            hs.Add(wx.Button(self, wx.ID_ANY, "Evaluate", name=str(i)), 1, wx.EXPAND)
            i+=1
            vs.Add(hs, 0, wx.EXPAND)
        self.SetSizer(vs)

            
#----------------------------------------------------------------------
class ReferencesPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour('#efefef')
        h1 = wx.StaticText(self, wx.ID_ANY,
                           "Variants with reference hits")
        h1.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.refs = controller.references.get_all_ref_records()
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(h1, 0, wx.ALL|wx.EXPAND, 10)
        sizer.Add(RefPanel(self, self.refs), 0, wx.EXPAND)
        self.SetSizer(sizer)
        self.is_changed = False
    def save_changes(self):
        for ref in self.refs:
            if ref.is_changed:
                controller.references.update_ref_record(ref)
                ref.is_changed = False
        self.is_changed = False


#----------------------------------------------------------------------
class MainFrame(wx.Frame):
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="genAP wb", size=(1024, 800))
        ref_panel = ReferencesPanel(self)
        
        self.Show()
        
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
