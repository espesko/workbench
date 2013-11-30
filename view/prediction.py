import wx
import controller.prediction


#----------------------------------------------------------------------
class PredHeaders(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(wx.StaticText(self, wx.ID_ANY, "Gene",
                                style=wx.NO_BORDER), 1, wx.EXPAND)
        sizer.Add(wx.StaticText(self, wx.ID_ANY, "Variant (HGVS)",
                                style=wx.NO_BORDER), 1, wx.EXPAND)
        sizer.Add(wx.StaticText(self, wx.ID_ANY, "type_of_mutation",
                                style=wx.NO_BORDER), 3, wx.EXPAND)
        sizer.Add(wx.StaticText(self, wx.ID_ANY, "comment",
                                style=wx.NO_BORDER), 3, wx.EXPAND)
        self.SetSizer(sizer)

#----------------------------------------------------------------------    
class PredCtrls(list):
    def __init__(self, parent, pred):
        list.__init__(self)
        self.pred = pred
        #Append xwCtrl and proportion:
        self.append((wx.TextCtrl(parent, wx.ID_ANY, pred["gene"],
                                 style=wx.NO_BORDER, name="gene"), 1))
        self.append((wx.TextCtrl(parent, wx.ID_ANY, pred["variant"],
                                 style=wx.NO_BORDER, name="variant"), 1))
        self.append((wx.TextCtrl(parent, wx.ID_ANY, pred["type_of_mutation"],
                                 style=wx.NO_BORDER, name="type_of_mutation"), 3))
        self.append((wx.TextCtrl(parent, wx.ID_ANY, pred["comment"],
                                 style=wx.NO_BORDER, name="comment"), 3))
        self[2][0].SetBackgroundColour(wx.RED) # just for illustration

#----------------------------------------------------------------------
class PredRow(wx.Panel):
    def __init__(self, parent, pred):
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)
        self.parent = parent
        self.pred = pred
        ctrls = PredCtrls(self, pred)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        for ctrl in ctrls:
            sizer.Add(ctrl[0], ctrl[1], wx.EXPAND)
        self.SetSizer(sizer)
        self.Bind(wx.EVT_TEXT, self.on_text)
    def on_text(self, event): # keep the PredView objects up to date when the user enters data
        ctrl = event.GetEventObject()
        ctrl.SetForegroundColour(wx.BLUE) # text turns blue when changed by user
        name = ctrl.GetName()
        value = ctrl.GetValue()
        self.pred[name] = value
        self.pred.is_changed = True
        self.parent.is_changed = True
      
#----------------------------------------------------------------------       
class PredictionPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour('#efefef')
        h1 = wx.StaticText(self, wx.ID_ANY,
                           "Likely pathogenic")
        h1.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.preds = controller.prediction.get_all_pred_records()
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(h1, 0, wx.ALL|wx.EXPAND, 10)
        sizer.Add(PredHeaders(self), 0, wx.ALL|wx.EXPAND,2)
        for pred in self.preds:
            sizer.Add(PredRow(self, pred), 0, wx.ALL|wx.EXPAND)
        self.SetSizer(sizer)
        self.is_changed = False
    def save_changes(self):
        for pred in self.preds:
            if pred.is_changed:
                controller.prediction.update_pred_record(pred)
                pred.is_changed = False
        self.is_changed = False


#----------------------------------------------------------------------
class MainFrame(wx.Frame):
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="genAP wb", size=(1024, 800))
        pred_panel = PredictionPanel(self)
        
        self.Show()
        
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
