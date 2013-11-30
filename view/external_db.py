import wx
import controller.external_db


#----------------------------------------------------------------------
class ExtDBHeaders(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(wx.StaticText(self, wx.ID_ANY, "Gene",
                                style=wx.NO_BORDER), 1, wx.EXPAND)
        sizer.Add(wx.StaticText(self, wx.ID_ANY, "Variant (HGVS)",
                                style=wx.NO_BORDER), 1, wx.EXPAND)
        sizer.Add(wx.StaticText(self, wx.ID_ANY, "bic",
                                style=wx.NO_BORDER), 1, wx.EXPAND)
        sizer.Add(wx.StaticText(self, wx.ID_ANY, "hgmd_pro",
                                style=wx.NO_BORDER), 1, wx.EXPAND)
        sizer.Add(wx.StaticText(self, wx.ID_ANY, "lovd",
                                style=wx.NO_BORDER), 1, wx.EXPAND)
        sizer.Add(wx.StaticText(self, wx.ID_ANY, "clin_var",
                                style=wx.NO_BORDER), 1, wx.EXPAND)
        sizer.Add(wx.StaticText(self, wx.ID_ANY, "omim",
                                style=wx.NO_BORDER), 1, wx.EXPAND)
        sizer.Add(wx.StaticText(self, wx.ID_ANY, "db_snp",
                                style=wx.NO_BORDER), 1, wx.EXPAND)
        self.SetSizer(sizer)

#----------------------------------------------------------------------    
class ExtDBCtrls(list):
    def __init__(self, parent, extdb):
        list.__init__(self)
        self.extdb = extdb
        #Append xwCtrl and proportion:
        self.append((wx.TextCtrl(parent, wx.ID_ANY, extdb["gene"],
                                    style=wx.NO_BORDER, name="gene"), 1))
        self.append((wx.TextCtrl(parent, wx.ID_ANY, extdb["variant"],
                                 style=wx.NO_BORDER, name="variant"), 1))
        self.append((wx.TextCtrl(parent, wx.ID_ANY, extdb["bic"],
                                 style=wx.NO_BORDER, name="bic"), 1))
        self.append((wx.TextCtrl(parent, wx.ID_ANY, extdb["hgmd_pro"],
                                 style=wx.NO_BORDER, name="hgmd_pro"), 1))
        self.append((wx.TextCtrl(parent, wx.ID_ANY, extdb["lovd"],
                                 style=wx.NO_BORDER, name="lovd"), 1))
        self.append((wx.TextCtrl(parent, wx.ID_ANY, extdb["clin_var"],
                                 style=wx.NO_BORDER, name="clin_var"), 1))
        self.append((wx.TextCtrl(parent, wx.ID_ANY, extdb["omim"],
                                 style=wx.NO_BORDER, name="omim"), 1))
        self.append((wx.TextCtrl(parent, wx.ID_ANY, extdb["db_snp"],
                                 style=wx.NO_BORDER, name="db_snp"), 1))

#----------------------------------------------------------------------
class ExtDBRow(wx.Panel):
    def __init__(self, parent, extdb):
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)
        self.parent = parent
        self.extdb = extdb
        ctrls = ExtDBCtrls(self, extdb)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        for ctrl in ctrls:
            sizer.Add(ctrl[0], ctrl[1], wx.EXPAND)
        self.SetSizer(sizer)
        self.Bind(wx.EVT_TEXT, self.on_text)
    def on_text(self, event): # keep the ExtDBView objects up to date when the user enters data
        ctrl = event.GetEventObject()
        ctrl.SetForegroundColour(wx.BLUE) # text turns blue when changed by user
        name = ctrl.GetName()
        value = ctrl.GetValue()
        self.extdb[name] = value
        self.extdb.is_changed = True
        self.parent.is_changed = True

#----------------------------------------------------------------------       
class ExternalDBPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour('#efefef')
        h1 = wx.StaticText(self, wx.ID_ANY,
                           "Variants with hits")
        h1.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.extdbs = controller.external_db.get_all_extdb_records()
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(h1, 0, wx.ALL|wx.EXPAND, 10)
        sizer.Add(ExtDBHeaders(self), 0, wx.ALL|wx.EXPAND,2)
        for extdb in self.extdbs:
            sizer.Add(ExtDBRow(self, extdb), 0, wx.ALL|wx.EXPAND)
        self.SetSizer(sizer)
        self.is_changed = False
    def save_changes(self):
        for extdb in self.extdbs:
            if extdb.is_changed:
                controller.external_db.update_extdb_record(extdb)
                extdb.is_changed = False
        self.is_changed = False


#----------------------------------------------------------------------
class MainFrame(wx.Frame):
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="genAP wb", size=(1024, 800))
        extdb_panel = ExternalDBPanel(self)
        
        self.Show()
        
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
