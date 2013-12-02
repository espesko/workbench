import wx
#import controller.refeval

def st(self, text):
    return wx.StaticText(self, wx.ID_ANY, text)
def rb(self, text=""):
    return wx.RadioButton(self, wx.ID_ANY, text)

#----------------------------------------------------------------------
class ButtonBar(wx.Panel):
    def __init__(self, parent, *argc):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        main_frame = self.GetTopLevelParent()
        buttons = []
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        for label in argc:
            button =wx.Button(self, wx.ID_ANY, label, name=label)
            button.Bind(wx.EVT_BUTTON, main_frame.on_button)
            buttons.append(button)
            sizer.Add(button, 1, wx.ALL, 20)
        self.SetSizer(sizer)

#----------------------------------------------------------------------
class EvalRow(wx.Panel):
    def __init__(self, parent, cat, evl, rbs, cb=0, score=0):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour('#ffffff')
        wx.StaticText(self, wx.ID_ANY, cat, pos=(3,3))
        if cb:
            wx.CheckBox(self, wx.ID_ANY, pos=(70, 3))
            self.Bind(wx.EVT_CHECKBOX, self.on_checked)
            self.SetForegroundColour("#999999")
        wx.StaticText(self, wx.ID_ANY, evl, pos=(100,3))
        pos = 220
        for rb in rbs:
            wx.RadioButton(self, wx.ID_ANY, rb, pos=(pos, 3))
            pos+=40
        if score:
            self.score = wx.TextCtrl(self, wx.ID_ANY, score, (340, 3),
                                     style=wx.TE_CENTER|wx.NO_BORDER)
            self.score.SetBackgroundColour("#efefef")
            if cb:
                self.score.SetForegroundColour("#999999")
            
    def on_checked(self, event):
        ctrl = event.GetEventObject()
        if ctrl.IsChecked():
            colour = "#000000"
        else:
            colour = "#999999"
        for ctrl in self.GetChildren():
            ctrl.Hide()
            ctrl.SetForegroundColour(colour)
            ctrl.Show()
        event.Skip()
        
#----------------------------------------------------------------------
class EvalPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.BORDER_SUNKEN)
        self.SetBackgroundColour('#efefef')
        s = wx.BoxSizer(wx.VERTICAL)

        hds = EvalRow(self, "Category", "Evaluation", (), 0, "Score")
        hds.SetBackgroundColour("#efefef")
        s.Add(hds, 0, wx.EXPAND)
        s.Add(EvalRow(self, "Relevance",
                            "Is reference \nrelevant?",
                           ("Yes", "No")), 0, wx.EXPAND)
        s.Add(EvalRow(self, "Conclusion",
                            "Does reference \nsupport pathogenicity?",
                           ("Yes", "No", "VUS")), 0, wx.EXPAND)
        s.Add(EvalRow(self, "Segregation",
                            "Consistent with \nconclusion?",
                           ("Yes", "No"), 1, "+5"), 0, wx.EXPAND)
        s.Add(EvalRow(self, "Protein",
                            "Abnormal protein \nfunction?",
                           ("Yes", "No"), 1, "..."), 0, wx.EXPAND)
        s.Add(EvalRow(self, "RNA",
                            "Abnormal splicing/\nprotein expression?",
                           ("Yes", "No"), 1, "..."), 0, wx.EXPAND)
        s.Add(EvalRow(self, "Gene coverage",
                            ">90% of gene \nsequenced?",
                           ("Yes", "No"), 0, "0"), 0, wx.EXPAND)
        s.Add(EvalRow(self, "Age of evidence \n(auto)",
                            "Reference <10 \nyears?",
                           ("Yes", "No"), 0, "0"), 0, wx.EXPAND)
        s.Add(EvalRow(self, "SUM",
                            "",
                           (""), 0, "+5"), 0, wx.EXPAND)
        s.Add(wx.StaticLine(self, wx.ID_ANY), 0, wx.EXPAND)
        s.Add(EvalRow(self, "Conclusion:\nHigh quality evidence?",
                            "",
                           ("Yes", "No", "IRRELEV/VUS")), 0, wx.EXPAND)
        s.Add(wx.StaticLine(self, wx.ID_ANY), 0, wx.EXPAND)
        s.Add(wx.Button(self, wx.ID_ANY, "Finish"), 0, wx.ALIGN_RIGHT)
        self.Bind(wx.EVT_BUTTON, self.on_finish)
        self.SetSizer(s)
    def on_finish(self, event):
        print "Saving evaluation"

#----------------------------------------------------------------------
class RefEvalPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour('#efefef')
        self.h_font = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, "")
        

    def new_obj(self, ref):
        self.ref = ref
        self.h1 = wx.StaticText(self, wx.ID_ANY, "Reference evaluation")
        self.h1.SetFont(self.h_font)
        h2 = "Selected reference: %s" % (ref['references'])
        self.h2 = wx.StaticText(self, wx.ID_ANY, h2)
        h3 = "Variant: %s %s" % (ref['gene'], ref['variant'])
        self.h3 = wx.StaticText(self, wx.ID_ANY, h3)
        self.eval_panel = EvalPanel(self)
        self.button_bar = ButtonBar(self, "<<<  Previous", "Next  >>>")
        self.show_all()

    def show_all(self):
        s = wx.BoxSizer(wx.VERTICAL)
        s.Add(self.h1, 0, wx.EXPAND|wx.ALL, 10)
        s.Add(self.h2, 0, wx.EXPAND|wx.LEFT, 10)
        s.Add(self.h3, 0, wx.EXPAND|wx.LEFT, 10)
        s.Add(self.eval_panel, 1, wx.EXPAND|wx.ALL, 10)
        s.Add(self.button_bar, 0, wx.EXPAND)
        self.SetSizer(s)
        self.Layout()
        


#----------------------------------------------------------------------
if __name__ == "__main__":
    class MainFrame(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None, title="genAP wb", size=(1024, 800))
            obj = {'references': "	Elsing et al 2011, PMID: 22904364",
                   'gene':'BRCA1',
                   'variant':'c.38T>C'}
            details_panel = RefEvalPanel(self)
            details_panel.new_obj(obj)
            self.Bind(wx.EVT_BUTTON, self.on_button)
            self.Show()
        def on_button(self, event):
            action = event.GetEventObject().GetName()
            print action
            return

    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()

