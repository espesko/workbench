import wx
from vardb import VarDBPanel, VarDBRow
from frequency import FrequencyPanel, FreqRow
from external_db import ExternalDBPanel, ExtDBRow
from prediction import PredictionPanel, PredRow
from references import ReferencesPanel, RefPanel
from details import DetailsPanel
from refeval import RefEvalPanel
from sample import SamplePanel
import controller.export


#----------------------------------------------------------------------
class Menubar(wx.MenuBar):
    def __init__(self, parent):
        wx.MenuBar.__init__(self)
        self.parent = parent
        self.file = wx.Menu()
        self.save = wx.MenuItem(self.file, wx.ID_ANY,
                    "Save changes", "", wx.ITEM_NORMAL)
        self.file.AppendItem(self.save)
        self.export = wx.MenuItem(self.file, wx.ID_ANY,
                    "Export", "", wx.ITEM_NORMAL)
        self.file.AppendItem(self.export)
        self.exit = wx.MenuItem(self.file, wx.ID_ANY,
                    "Exit", "", wx.ITEM_NORMAL)
        self.file.AppendItem(self.exit)
        self.Append(self.file, "File")
        self.options = wx.Menu()
        self.vdb_threshold = wx.MenuItem(self.options, wx.ID_ANY,
                    "Set age threshold (VarDB)", "", wx.ITEM_NORMAL)
        self.options.AppendItem(self.vdb_threshold)
        self.options.Append(wx.ID_ANY,
                    "Set neutrality threshold (Frequency)", "", wx.ITEM_NORMAL)
        self.Append(self.options, "Options")
        self.help = wx.Menu()
        self.user_guide = wx.MenuItem(self.help, wx.ID_ANY,
                    "User guide", "", wx.ITEM_NORMAL)
        self.help.AppendItem(self.user_guide)
        self.context_help = wx.MenuItem(self.help, wx.ID_ANY,
                    "Context speciffic help", "", wx.ITEM_NORMAL)
        self.help.AppendItem(self.context_help)
        self.Append(self.help, "Help")
        parent.SetMenuBar(self)
        parent.Bind(wx.EVT_MENU, self.on_menu, self)
    def message_dialog(self, cap, text):
            dlg = wx.MessageDialog(self, text, cap)
            dlg.ShowModal()
            dlg.Destroy()
    def on_menu(self, event):
        selection = event.GetSelection()
        if selection == 100: # save changes
            if self.parent.save_changes() == "NO_CHANGES":
                self.message_dialog("Save", "No changes to save")
        elif selection == 101: # export
            filename = controller.export.export_all()
            self.message_dialog("Export succeeded", "Filename: " + filename)
        elif selection == 102: # exit
            self.parent.close()
        elif selection == 103: # options
            self.message_dialog("Option", "Not implemented")
        elif selection == 104: # options
            self.message_dialog("Option", "Not implemented")
        elif selection == 105: # help
            self.message_dialog("Help", "Not implemented")
        elif selection == 106: # help
            self.message_dialog("Help", "Not implemented")
        event.Skip() 
                

#----------------------------------------------------------------------
class VarDBTab(wx.Panel): 
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.main_panel = VarDBPanel(self)
        self.side_panel = DetailsPanel(self)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.main_panel, 3, wx.ALL|wx.EXPAND, 2)
        self.sizer.Add(wx.StaticLine(self, wx.ID_ANY,
                                style=wx.LI_VERTICAL), 0, wx.ALL|wx.EXPAND, 0)
        self.sizer.Add(self.side_panel, 1, wx.ALL|wx.EXPAND, 2)
        self.SetSizer(self.sizer)
        self.Bind(wx.EVT_CHILD_FOCUS, self.on_select_variant)
    def on_select_variant(self, event):
        obj = event.GetEventObject()
        if type(obj) == VarDBRow:
            self.side_panel.new_obj(obj.vdb)
        event.Skip() 
    def is_changed(self):
        return self.main_panel.is_changed
    def save_changes(self):
        self.main_panel.save_changes()
       
#----------------------------------------------------------------------
class FrequencyTab(wx.Panel): 
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.main_panel = FrequencyPanel(self)
        self.side_panel = DetailsPanel(self)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.main_panel, 3, wx.ALL|wx.EXPAND, 2)
        self.sizer.Add(wx.StaticLine(self, wx.ID_ANY,
                                style=wx.LI_VERTICAL), 0, wx.ALL|wx.EXPAND, 0)
        self.sizer.Add(self.side_panel, 1, wx.ALL|wx.EXPAND, 2)
        self.SetSizer(self.sizer)
        self.Bind(wx.EVT_CHILD_FOCUS, self.on_select_variant)
    def on_select_variant(self, event):
        obj = event.GetEventObject()
        if type(obj) == FreqRow:
            self.side_panel.new_obj(obj.freq)
        event.Skip() 
    def is_changed(self):
        return self.main_panel.is_changed
    def save_changes(self):
        self.main_panel.save_changes()
        
#----------------------------------------------------------------------
class ExternalDBTab(wx.Panel): 
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.main_panel = ExternalDBPanel(self)
        self.side_panel = DetailsPanel(self)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.main_panel, 3, wx.ALL|wx.EXPAND, 2)
        self.sizer.Add(wx.StaticLine(self, wx.ID_ANY,
                                style=wx.LI_VERTICAL), 0, wx.ALL|wx.EXPAND, 0)
        self.sizer.Add(self.side_panel, 1, wx.ALL|wx.EXPAND, 2)
        self.SetSizer(self.sizer)
        self.Bind(wx.EVT_CHILD_FOCUS, self.on_select_variant)
    def on_select_variant(self, event):
        obj = event.GetEventObject()
        if type(obj) == ExtDBRow:
            self.side_panel.new_obj(obj.extdb)
        event.Skip() 
    def is_changed(self):
        return self.main_panel.is_changed
    def save_changes(self):
        self.main_panel.save_changes()
        
#----------------------------------------------------------------------
class PredictionTab(wx.Panel): 
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.main_panel = PredictionPanel(self)
        self.side_panel = DetailsPanel(self)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.main_panel, 3, wx.ALL|wx.EXPAND, 2)
        self.sizer.Add(wx.StaticLine(self, wx.ID_ANY,
                                style=wx.LI_VERTICAL), 0, wx.ALL|wx.EXPAND, 0)
        self.sizer.Add(self.side_panel, 1, wx.ALL|wx.EXPAND, 2)
        self.SetSizer(self.sizer)
        self.Bind(wx.EVT_CHILD_FOCUS, self.on_select_variant)
    def on_select_variant(self, event):
        obj = event.GetEventObject()
        if type(obj) == PredRow:
            self.side_panel.new_obj(obj.pred)
        event.Skip() 
    def is_changed(self):
        return self.main_panel.is_changed
    def save_changes(self):
        self.main_panel.save_changes()
        
#----------------------------------------------------------------------
class ReferencesTab(wx.Panel): 
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.main_panel = ReferencesPanel(self)
        self.side_panel = RefEvalPanel(self)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.main_panel, 2, wx.ALL|wx.EXPAND, 2)
        self.sizer.Add(wx.StaticLine(self, wx.ID_ANY,
                                style=wx.LI_VERTICAL), 0, wx.ALL|wx.EXPAND, 0)
        self.sizer.Add(self.side_panel, 1, wx.ALL|wx.EXPAND, 2)
        self.SetSizer(self.sizer)
        self.Bind(wx.EVT_BUTTON, self.on_evaluate)
 
    def on_evaluate(self, event):
        index = int(event.GetEventObject().GetName())
        ref = self.main_panel.refs[index]
        self.side_panel.new_obj(ref)
        event.Skip()
    def is_changed(self):
        return self.main_panel.is_changed
    def save_changes(self):
        self.main_panel.save_changes()
        
#----------------------------------------------------------------------
class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="genAP wb", size=(1400, 800))
        self.menu_bar = Menubar(self)
        self.notebook = wx.Notebook(self, wx.ID_ANY, style=0)
        self.sample_tab = SamplePanel(self.notebook)
        self.notebook.AddPage(self.sample_tab, "Sample")
        self.status_bar = self.CreateStatusBar(1, 0)
        self.Show()

    def show_all(self):
        page_count = self.notebook.GetPageCount()
        for i in range(page_count-1): # keep sample page only
            self.notebook.RemovePage(1)
        self.vardb_tab = VarDBTab(self.notebook)
        self.frequency_tab = FrequencyTab(self.notebook)
        self.external_db_tab = ExternalDBTab(self.notebook)
        self.prediction_tab = PredictionTab(self.notebook)
        self.references_tab = ReferencesTab(self.notebook)
        self.notebook.AddPage(self.vardb_tab, "VarDB")
        self.notebook.AddPage(self.frequency_tab, "Frequency")
        self.notebook.AddPage(self.external_db_tab, "External DB")
        self.notebook.AddPage(self.prediction_tab, "Prediction")
        self.notebook.AddPage(self.references_tab, "References")
        sample = self.sample_tab.sample
        self.status_bar.SetStatusText("Sample %s loaded | Gene Panel: %s" %
                                      (sample["sample"], sample["panel"]))
        self.Show()
    def close(self):
        if self.save_changes() != wx.ID_CANCEL:
            wx.Frame.Close(self)
    def save_changes(self):
        stat = "NO_CHANGES"
        if self.notebook.GetPageCount() == 1:
            return stat
        if self.vardb_tab.is_changed():
            stat = self.save_tab(1, "VarDB entries have changed") 
            if stat == wx.ID_CANCEL:
                return stat
        if self.frequency_tab.is_changed():
            stat = self.save_tab(2, "Frequency entries have changed") 
            if stat == wx.ID_CANCEL:
                return stat
        if self.external_db_tab.is_changed():
            stat = self.save_tab(3, "External DB entries have changed") 
            if stat == wx.ID_CANCEL:
                return stat
        if self.prediction_tab.is_changed():
            stat = self.save_tab(4, "Prediction entries have changed")
        return stat
    def save_tab(self, tab, cap=""):
        page = self.notebook.GetPage(tab)
        self.notebook.ChangeSelection(tab)
        dlg = wx.MessageDialog(self, "Save changes?", cap,
                               wx.YES_NO|wx.CANCEL|wx.ICON_QUESTION)
        choice = dlg.ShowModal()
        if choice == wx.ID_YES:
            page.save_changes()
        dlg.Destroy()
        return choice
    def on_button(self, event):
        action = event.GetEventObject().GetName()
        if action == "<<<  Previous":
            self.notebook.AdvanceSelection(forward = False)
        elif action == "Next  >>>":
            self.notebook.AdvanceSelection()
        else:
            print "Action: ", action


#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
