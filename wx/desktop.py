#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Thu Feb 11 04:08:55 2010

import wx
import webbrowser
import wx.lib.iewin_old as iewin
import wx.lib.sized_controls as sc
import config
import update
import time
import httplib
import os

# begin wxGlade: extracode
# end wxGlade



class UpdatedDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: UpdatedDialog.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.label_updated = wx.StaticText(self, -1, "Your Database is up to date.")
        self.button_updated_ok = wx.Button(self, wx.ID_OK, "")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: UpdatedDialog.__set_properties
        self.SetTitle("Your DB is up to date")
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: UpdatedDialog.__do_layout
        sizer_updated = wx.BoxSizer(wx.VERTICAL)
        sizer_updated.Add(self.label_updated, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        sizer_updated.Add(self.button_updated_ok, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.SetSizer(sizer_updated)
        sizer_updated.Fit(self)
        self.Layout()
        # end wxGlade

# end of class UpdatedDialog

class ConfigDialog(sc.SizedDialog):
    def __init__(self, parent, id, title):
        sc.SizedDialog.__init__(self, None, -1, title, 
                        style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        
        self.pane = self.GetContentsPane()
        self.pane.SetSizerType("form")
        
        # row port
        wx.StaticText(self.pane, -1, "Port")
        self.textCtrl_port = wx.TextCtrl(self.pane, -1, config.SS_PORT)
        self.textCtrl_port.SetSizerProps(expand=True)

        # row timestamp
        wx.StaticText(self.pane, -1, "TimeStamp(GMT)")
	dt = time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(int(config.SS_DB_UPDTIME)))
        self.textCtrl_updt = wx.TextCtrl(self.pane, -1, dt)
        self.textCtrl_updt.SetSizerProps(expand=True)
        
	# row threads
        wx.StaticText(self.pane, -1, "Max Number of Threads(VeryCD only)")
        self.textCtrl_mt = wx.TextCtrl(self.pane, -1, config.SS_MAX_THREADS)
        self.textCtrl_mt.SetSizerProps(expand=True)
              
        # row title
        wx.StaticText(self.pane, -1, "Update From(simplecd is usually 4-5 times faster)")
        # here's how to add a 'nested sizer' using sized_controls
        self.radioPane = sc.SizedPanel(self.pane, -1)
        self.radioPane.SetSizerType("horizontal")
        self.radioPane.SetSizerProps(expand=True)        
        # make these children of the radioPane to have them use
        # the horizontal layout
        self.rb1 = wx.RadioButton(self.radioPane, -1, "SimpleCD")
        self.rb2 = wx.RadioButton(self.radioPane, -1, "VeryCD")
        if config.SS_UPDATE_SOURCE == 'simplecd':
            self.rb1.SetValue(True)
        elif config.SS_UPDATE_SOURCE == 'verycd':
            self.rb2.SetValue(True)
        # end row title
        
        # add dialog buttons
        self.SetButtonSizer(self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL))
        self.Bind(wx.EVT_BUTTON,self.onOK,id=wx.ID_OK)
        
        # a little trick to make sure that you can't resize the dialog to
        # less screen space than the controls need
        self.Fit()
        self.SetMinSize(self.GetSize())

    def onOK(self,event):
        config.SS_PORT = self.textCtrl_port.GetValue()
        try:
            config.SS_DB_UPDTIME = str(int(time.mktime(time.strptime(self.textCtrl_updt.GetValue(),'%Y/%m/%d %H:%M:%S'))))
        except Exception as what:
            print what.__str__()
        config.SS_MAX_THREADS = self.textCtrl_mt.GetValue()
        config.SS_UPDATE_SOURCE = self.rb2.GetValue() and 'verycd' or 'simplecd'
        config.savecfg()
        self.Close()


class AboutFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: AboutFrame.__init__
        kwds["style"] = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.SYSTEM_MENU
        wx.Frame.__init__(self, *args, **kwds)
        self.about_png = wx.StaticBitmap(self, -1, wx.Bitmap("res\\about_dialog.png", wx.BITMAP_TYPE_ANY))
        self.Visit = wx.Button(self, -1, "Visit Homepage")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.visit_home_handler, self.Visit)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: AboutFrame.__set_properties
        self.SetTitle("About SimpleCD Desktop")
        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap(wx.Bitmap("res\\logo.png", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)
        self.SetSize((480, 320))
        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.about_png.SetBackgroundColour(wx.Colour(255, 255, 255))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: AboutFrame.__do_layout
        sizer_about = wx.BoxSizer(wx.VERTICAL)
        sizer_about.Add(self.about_png, 0, wx.ALL, 10)
        sizer_about.Add(self.Visit, 0, wx.RIGHT|wx.ALIGN_RIGHT|wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_VERTICAL, 20)
        self.SetSizer(sizer_about)
        self.Layout()
        # end wxGlade

    def visit_home_handler(self, event): # wxGlade: AboutFrame.<event_handler>
        webbrowser.open_new_tab('http://www.simplecd.org')


# end of class AboutFrame


class MainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # run web server
        #config.run_server()

        # begin wxGlade: MainFrame.__init__
        kwds["style"] = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.MAXIMIZE_BOX|wx.SYSTEM_MENU|wx.RESIZE_BORDER|wx.FULL_REPAINT_ON_RESIZE|wx.CLIP_CHILDREN
        wx.Frame.__init__(self, *args, **kwds)
        
        # Menu Bar
        self.frame_main_menubar = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(3001, "Home", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(wx.ID_SAVEAS, "Save as", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendSeparator()
        wxglade_tmp_menu.Append(wx.ID_EXIT, "Exit", "", wx.ITEM_NORMAL)
        self.frame_main_menubar.Append(wxglade_tmp_menu, "File")
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(3002, "Search", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(3003, "Ranking", "", wx.ITEM_NORMAL)
        self.frame_main_menubar.Append(wxglade_tmp_menu, "View")
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(3004, "Config", "", wx.ITEM_NORMAL)
        self.frame_main_menubar.Append(wxglade_tmp_menu, "Config")
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(3007, "Update from ...", "", wx.ITEM_NORMAL)
        self.frame_main_menubar.Append(wxglade_tmp_menu, "DB")
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(3006, "Help", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(3005, "Update", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(wx.ID_ABOUT, "About", "", wx.ITEM_NORMAL)
        self.frame_main_menubar.Append(wxglade_tmp_menu, "Help")
        self.SetMenuBar(self.frame_main_menubar)
        # Menu Bar end
        self.frame_main_statusbar = self.CreateStatusBar(1, 0)
        
        # Tool Bar
        self.frame_main_toolbar = wx.ToolBar(self, -1, style=wx.TB_HORIZONTAL|wx.TB_DOCKABLE|wx.TB_3DBUTTONS)
        self.SetToolBar(self.frame_main_toolbar)
        self.frame_main_toolbar.AddLabelTool(2001, "Home", wx.Bitmap("res\\homepage.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "Home", "")
        self.frame_main_toolbar.AddLabelTool(2002, "Search", wx.Bitmap("res\\search.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "Search", "")
        self.frame_main_toolbar.AddLabelTool(2003, "Ranking", wx.Bitmap("res\\ranking.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "Ranking", "")
        self.frame_main_toolbar.AddSeparator()
        self.frame_main_toolbar.AddLabelTool(2004, "Config", wx.Bitmap("res\\config.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "Config", "")
        self.frame_main_toolbar.AddLabelTool(2005, "Update", wx.Bitmap("res\\update.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "Update", "")
        self.frame_main_toolbar.AddSeparator()
        self.frame_main_toolbar.AddLabelTool(wx.ID_ABOUT, "About", wx.Bitmap("res\\about.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "About", "")
        # Tool Bar end

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_MENU, self.home_handler, id=3001)
        self.Bind(wx.EVT_MENU, self.saveas_handler, id=wx.ID_SAVEAS)
        self.Bind(wx.EVT_MENU, self.exit_handler, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.search_handler, id=3002)
        self.Bind(wx.EVT_MENU, self.ranking_handler, id=3003)
        self.Bind(wx.EVT_MENU, self.config_handler, id=3004)
        self.Bind(wx.EVT_MENU, self.db_update_handler, id=3007)
        self.Bind(wx.EVT_MENU, self.help_handler, id=3006)
        self.Bind(wx.EVT_MENU, self.update_handler, id=3005)
        self.Bind(wx.EVT_MENU, self.about_handler, id=wx.ID_ABOUT)
        self.Bind(wx.EVT_TOOL, self.home_handler, id=2001)
        self.Bind(wx.EVT_TOOL, self.search_handler, id=2002)
        self.Bind(wx.EVT_TOOL, self.ranking_handler, id=2003)
        self.Bind(wx.EVT_TOOL, self.config_handler, id=2004)
        self.Bind(wx.EVT_TOOL, self.update_handler, id=2005)
        self.Bind(wx.EVT_TOOL, self.about_handler, id=wx.ID_ABOUT)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MainFrame.__set_properties
        self.SetTitle("SimpleCD Desktop 0.1.2c")
        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap(wx.Bitmap("res\\logo.png", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)
        self.SetSize((900, 599))
        self.SetFocus()
        self.frame_main_statusbar.SetStatusWidths([-1])
        # statusbar fields
        frame_main_statusbar_fields = ["Welcome to SimpleCD Desktop"]
        for i in range(len(frame_main_statusbar_fields)):
            self.frame_main_statusbar.SetStatusText(frame_main_statusbar_fields[i], i)
        self.frame_main_toolbar.SetToolBitmapSize((32, 32))
        self.frame_main_toolbar.Realize()
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MainFrame.__do_layout
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer_main)
        self.Layout()
        self.Centre()
        # end wxGlade

        # add homepage
        self.ie = iewin.IEHtmlWindow(self)
        sizer_main.Add(self.ie, 1, wx.GROW)
	self.ie.LoadUrl('http://localhost:%s/'%config.SS_PORT)

    def saveas_handler(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `saveas_handler' not implemented!"
        event.Skip()

    def exit_handler(self, event): # wxGlade: MainFrame.<event_handler>
        self.Close()

    def config_handler(self, event): # wxGlade: MainFrame.<event_handler>
        dialog_config = ConfigDialog(None, -1, "Configurations")
        app.SetTopWindow(dialog_config)
        dialog_config.ShowModal()
        dialog_config.Destroy()

    def about_handler(self, event): # wxGlade: MainFrame.<event_handler>
        frame_about = AboutFrame(None, -1, "")
        app.SetTopWindow(frame_main)
        frame_about.Show()

    def home_handler(self, event): # wxGlade: MainFrame.<event_handler>
        self.ie.LoadUrl('http://localhost:%s/'%config.SS_PORT)

    def ranking_handler(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `ranking_handler' not implemented!"
        event.Skip()

    def search_handler(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `search_handler' not implemented"
        event.Skip()

    def update_handler(self, event): # wxGlade: MainFrame.<event_handler>
        ids = update.get_update_ids()
        if len(ids) == 0:
            dialog_updated = UpdatedDialog(None, -1, "")
            app.SetTopWindow(dialog_updated)
            dialog_updated.ShowModal()
            dialog_updated.Destroy()
            return
        elif ids[0].startswith('new:'):
            dlg = wx.MessageDialog(self, ids[0][4:],
                               'Update Error',
                               wx.OK | wx.ICON_INFORMATION
                               #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
            dlg.ShowModal()
            dlg.Destroy()
        elif config.SS_UPDATE_SOURCE == 'verycd':
            max = len(ids)
            print max
            dlg = wx.ProgressDialog("Updating Databases...",
                               'Processing 1/%d' % (max*2/3),
                               maximum = max,
                               parent=self,
                               style = wx.PD_CAN_ABORT
                                | wx.PD_APP_MODAL
                                | wx.PD_ELAPSED_TIME
                                | wx.PD_ESTIMATED_TIME
                                #| wx.PD_REMAINING_TIME
                                )
            import fetchvc
            lastid = fetchvc.update_ids(ids,dlg.Update,max)
            print lastid
            dlg.Update(max,'Finished')
            update.update_db_updtime(lastid)
            dlg.Destroy()
        elif config.SS_UPDATE_SOURCE == 'simplecd':
            group = 5
            max = ((len(ids)-1)/group+1)*3*2
            dlg = wx.ProgressDialog("Updating Databases...",
                               "Downloading 1/%d"%(max/2),
                               maximum = max,
                               parent=self,
                               style = wx.PD_CAN_ABORT
                                | wx.PD_APP_MODAL
                                | wx.PD_ELAPSED_TIME
                                | wx.PD_ESTIMATED_TIME
                                #| wx.PD_REMAINING_TIME
                                )
            keepGoing = True
            count = 0
            httpconn = httplib.HTTPConnection("www.simplecd.org")
            # group ids, 100 per group
            for i in range(0,max/3/2):
                subids = ids[i*group:i*group+group]
                for dbname in ['verycd','lock']:
                    update.download_updates(dbname,subids,httpconn=httpconn)
                    count += 1
                    (keepGoing, skip) = dlg.Update(count, "Downloading %d/%d"%(count,max/2))
                    if not keepGoing:
                        break
                if not keepGoing:
                    break
    	    # Apply_updates
    	    update.apply_updates('verycd',dlg.Update,max)
    	    #update.apply_updates('comment',dlg.Update,max)
	    open(config.SS_HOME_DIR+'/comment.updates','w').write('')
    	    update.apply_updates('lock',dlg.Update,max)
    	    dlg.Update(max,'Finished')
    	    # others
    	    if not update.delete_tempfiles().startswith('error'):
                update.update_db_updtime(ids[i*group-1])
                if i>=max/6:
                    print ids
                    update.update_db_updtime(ids[-1])
    	    dlg.Destroy()
        
    def help_handler(self, event): # wxGlade: MainFrame.<event_handler>
        webbrowser.open_new_tab('http://www.simplecd.org/bbs/')

    def db_update_handler(self, event): # wxGlade: MainFrame.<event_handler>
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(), 
            defaultFile="",
            wildcard="targz files (*.tar.gz)|*.tar.gz",
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
            )
        paths = None
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
        dlg.Destroy()
        updts = paths
        if updts:
            max = len(updts)*3*100000
            dlg = wx.ProgressDialog("Updating from files...",
                               "Extracting...Please be patient ",
                               maximum = max,
                               parent=self,
                               style = wx.PD_CAN_ABORT
                                | wx.PD_APP_MODAL
                                | wx.PD_ELAPSED_TIME
                                | wx.PD_ESTIMATED_TIME
                                #| wx.PD_REMAINING_TIME
                                )
            count = 1
            for updt in updts:
                import tarfile
                tar = tarfile.open(updt)
                tar.extractall(path=config.SS_HOME_DIR)
                tar.close()               
                update.apply_updates('verycd',dlg.Update,max-1) 
                update.apply_updates('comment',dlg.Update,max-1)
                update.apply_updates('lock',dlg.Update,max-1)
            dlg.Update(max,'Finished')
            update.delete_tempfiles()
            update.update_timestamp()
	    dlg.Destroy()


# end of class MainFrame

if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_main = MainFrame(None, -1, "")
    app.SetTopWindow(frame_main)
    frame_main.Show()
    app.MainLoop()
    config.stop_server()
