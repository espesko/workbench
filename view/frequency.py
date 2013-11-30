import wx
import controller.frequency


#----------------------------------------------------------------------
class FreqHeaders(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(wx.StaticText(self, wx.ID_ANY, "Gene",
                                style=wx.NO_BORDER), 1, wx.EXPAND)
        sizer.Add(wx.StaticText(self, wx.ID_ANY, "Variant (HGVS)",
                                style=wx.NO_BORDER), 1, wx.EXPAND)
        sizer.Add(wx.StaticText(self, wx.ID_ANY, "Norvariome",
                                style=wx.NO_BORDER), 1, wx.EXPAND)
        sizer.Add(wx.StaticText(self, wx.ID_ANY, "ESP65000",
                                style=wx.NO_BORDER), 1, wx.EXPAND)
        sizer.Add(wx.StaticText(self, wx.ID_ANY, "1000G",
                                style=wx.NO_BORDER), 1, wx.EXPAND)
        sizer.Add(wx.StaticText(self, wx.ID_ANY, "Contradictory information",
                                style=wx.NO_BORDER), 2, wx.EXPAND)
        sizer.Add(wx.StaticText(self, wx.ID_ANY, "Filter out",
                                style=wx.NO_BORDER), 1, wx.EXPAND)
        self.SetSizer(sizer)

#----------------------------------------------------------------------    
class FreqCtrls(list):
    def __init__(self, parent, freq):
        list.__init__(self)
        self.freq = freq
        self.append((wx.TextCtrl(parent, wx.ID_ANY, freq["gene"],
                                 style=wx.NO_BORDER, name="gene"), 1))
        self.append((wx.TextCtrl(parent, wx.ID_ANY, freq["variant"],
                                 style=wx.NO_BORDER, name="variant"), 1))
        self.append((wx.TextCtrl(parent, wx.ID_ANY, str(freq["norvariome"]),
                                 style=wx.NO_BORDER, name="norvariome"), 1))
        self.append((wx.TextCtrl(parent, wx.ID_ANY, str(freq["esp65000"]),
                                 style=wx.NO_BORDER, name="esp65000"), 1))
        self.append((wx.TextCtrl(parent, wx.ID_ANY, str(freq["thousand_g"]),
                                 style=wx.NO_BORDER, name="thousand_g"), 1))
        self.append((wx.TextCtrl(parent, wx.ID_ANY, freq["contradictory"],
                                 style=wx.NO_BORDER|wx.TE_MULTILINE,
                                 name="contradictory"), 2))
        self.append((wx.CheckBox(parent, wx.ID_ANY, "",
                                      style=wx.NO_BORDER), 1))
        for ctrl in self: # add colours for illustration
            val = ctrl[0].GetLabel()
            if not val.lstrip("0.").isdigit():
                continue
            if float(val)>0.01:
                colour = "#007700"
            elif float(val)>0.001:
                colour = "#00dd00"
            else:
                colour = wx.WHITE
            ctrl[0].SetBackgroundColour(colour)

#----------------------------------------------------------------------
class FreqRow(wx.Panel):
    def __init__(self, parent, freq):
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)
        self.parent = parent
        self.freq = freq
        ctrls = FreqCtrls(self, freq)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        for ctrl in ctrls:
            sizer.Add(ctrl[0], ctrl[1], wx.EXPAND)
        self.SetSizer(sizer)
        self.Bind(wx.EVT_TEXT, self.on_text)
    def on_text(self, event): # keep the FreqView objects up to date when the user enters data
        ctrl = event.GetEventObject()
        ctrl.SetForegroundColour(wx.BLUE) # text turns blue when changed by user
        name = ctrl.GetName()
        value = ctrl.GetValue()
        self.freq[name] = value
        self.freq.is_changed = True
        self.parent.is_changed = True

#----------------------------------------------------------------------       
class FrequencyPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour('#efefef')
        h1 = wx.StaticText(self, wx.ID_ANY,
                           "Neutral variants (>0.01)")
        h1.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        h2 = wx.StaticText(self, wx.ID_ANY,
                           "Probably neutral variants (0.001-0.01)")
        h2.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.freqs = controller.frequency.get_all_freq_records()
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(h1, 0, wx.ALL|wx.EXPAND, 10)
        sizer.Add(FreqHeaders(self), 0, wx.ALL|wx.EXPAND,2)
        for freq in self.freqs:
            if not freq["neutral"]:
                continue
            sizer.Add(FreqRow(self, freq), 0, wx.ALL|wx.EXPAND)
        sizer.Add(h2, 0, wx.ALL|wx.EXPAND, 10)
        sizer.Add(FreqHeaders(self), 0, wx.ALL|wx.EXPAND,2)
        for freq in self.freqs:
            if freq["neutral"]:
                continue
            sizer.Add(FreqRow(self, freq), 0, wx.ALL|wx.EXPAND)
        self.SetSizer(sizer)
        self.is_changed = False
    def save_changes(self):
        for freq in self.freqs:
            if freq.is_changed:
                controller.frequency.update_freq_record(freq)
                freq.is_changed = False
        self.is_changed = False

#----------------------------------------------------------------------
class MainFrame(wx.Frame):
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="genAP wb", size=(1024, 800))
        freq_panel = FrequencyPanel(self)
        
        self.Show()
        
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
