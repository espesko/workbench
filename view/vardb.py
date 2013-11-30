import wx
import controller.vardb

#----------------------------------------------------------------------
class VarDBHeaders(wx.Panel):
    def __init__(self, parent, valid=True):
        wx.Panel.__init__(self, parent)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(wx.StaticText(self, wx.ID_ANY, "Gene",
                                style=wx.NO_BORDER), 1, wx.EXPAND)
        sizer.Add(wx.StaticText(self, wx.ID_ANY, "Variant (HGVS)",
                                style=wx.NO_BORDER), 1, wx.EXPAND)
        sizer.Add(wx.StaticText(self, wx.ID_ANY, "VarDB",
                                style=wx.NO_BORDER), 1, wx.EXPAND)
        sizer.Add(wx.StaticText(self, wx.ID_ANY, "Summary conclusion",
                                style=wx.NO_BORDER), 4, wx.EXPAND)
        sizer.Add(wx.StaticText(self, wx.ID_ANY, "Last VarDB check",
                                style=wx.NO_BORDER), 1, wx.EXPAND)
        if valid:
            sizer.Add(wx.StaticText(self, wx.ID_ANY, "Accept conclusion",
                                    style=wx.NO_BORDER), 1, wx.EXPAND)
        else:
            sizer.AddStretchSpacer()
        self.SetSizer(sizer)

#----------------------------------------------------------------------    
class VarDBCtrls(list):
    def __init__(self, parent,vdb):
        list.__init__(self)
        self.vdb = vdb
        self.append((wx.TextCtrl(parent, wx.ID_ANY, vdb["gene"],
                                 style=wx.NO_BORDER, name="gene"), 1))
        self.append((wx.TextCtrl(parent, wx.ID_ANY, vdb["variant"],
                                 style=wx.NO_BORDER, name="variant"), 1))
        self.append((wx.TextCtrl(parent, wx.ID_ANY, vdb["var_db"],
                                 style=wx.NO_BORDER, name="var_db"), 1))
        self.append((wx.TextCtrl(parent, wx.ID_ANY, vdb["summary"],
                                 style=wx.NO_BORDER|wx.TE_MULTILINE,
                                 name="summary"), 4))
        self.append((wx.TextCtrl(parent, wx.ID_ANY, str(vdb["last_check"]),
                                 style=wx.NO_BORDER, name="last_check"), 1))
        if vdb["valid"]:
            self.append((wx.CheckBox(parent, wx.ID_ANY, "",
                                      style=wx.NO_BORDER), 1))

#----------------------------------------------------------------------
class VarDBRow(wx.Panel):
    def __init__(self, parent, vdb):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.vdb = vdb
        ctrls = VarDBCtrls(self, vdb)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        for ctrl in ctrls:
            sizer.Add(ctrl[0], ctrl[1], wx.EXPAND)
        if not vdb["valid"]:
            sizer.AddStretchSpacer()
        self.SetSizer(sizer)
        self.Fit()
        self.Bind(wx.EVT_TEXT, self.on_text)
    def on_text(self, event): # keep the VarDBView objects up to date when the user enters data
        ctrl = event.GetEventObject()
        ctrl.SetForegroundColour(wx.BLUE) # text turns blue when changed by user
        name = ctrl.GetName()
        value = ctrl.GetValue()
        self.vdb[name] = value
        self.vdb.is_changed = True
        self.parent.is_changed = True
      
#----------------------------------------------------------------------       
class VarDBPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour('#efefef')
        h1 = wx.StaticText(self, wx.ID_ANY,
                           "Pre-classified (in-house) variants - STILL VALID")
        h1.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        h2 = wx.StaticText(self, wx.ID_ANY,
                           "Pre-classified (in-house) variants - OLD: RECHECK")
        h2.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.vdbs = controller.vardb.get_all_vardb_records()
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(h1, 0, wx.ALL|wx.EXPAND, 10)
        sizer.Add(VarDBHeaders(self), 0, wx.ALL|wx.EXPAND,2)
        for vdb in self.vdbs:
            if not vdb["valid"]:
                continue
            sizer.Add(VarDBRow(self, vdb), 0, wx.ALL|wx.EXPAND, 2)
        sizer.Add(h2, 0, wx.ALL|wx.EXPAND, 10)
        sizer.Add(VarDBHeaders(self, 0), 0, wx.ALL|wx.EXPAND,2)
        for vdb in self.vdbs:
            if vdb["valid"]:
                continue
            sizer.Add(VarDBRow(self, vdb), 0, wx.ALL|wx.EXPAND, 2)
        self.SetSizer(sizer)
        self.Fit()
        self.is_changed = False
    def save_changes(self):
        for vdb in self.vdbs:
            if vdb.is_changed:
                controller.vardb.update_vardb_record(vdb)
                vdb.is_changed = False
        self.is_changed = False
                
#----------------------------------------------------------------------
class MainFrame(wx.Frame):
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="genAP wb", size=(1024, 800))
        vardb_panel = VarDBPanel(self)
        
        self.Show()
        
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
