#!/usr/bin/env python
import wx
from os import sep, getcwd, stat, chdir, mkdir, makedirs
import sys
from shutil import rmtree, copytree
from location import _userbase_dir, dyn_dir, _home
from mercurial import ui, hg, commands, repo, revlog, cmdutil, util

def exists(path):
    try:
        stat(path)
        return True
    except: return False

cwd = getcwd()
chdir(cwd)

class Term2Win(object):
    # A stdout redirector.  Allows the messages from Mercurial to be seen in the Install Window
    def write(self, text):
        log.AppendText(text)
        wx.Yield()
        sys.__stdout__.write(text)

class InstallWindow(wx.Frame):
    def __init__(self):
        super(InstallWindow, self).__init__(None, wx.ID_ANY, "OpenRPG Setup Wizard")
        global log
        log = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_MULTILINE | wx.TE_READONLY)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(log, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        self.SetSize((640, 480))
        sys.stdout = Term2Win()
        self.ui = ui.ui()
        wx.CallAfter(self.install)

    def install(self):
        if exists(_userbase_dir+sep):
            count = 1
            while exists(_userbase_dir+'-'+str(count)): count += 1
            new_sys = _userbase_dir+'-'+str(count)
            copytree(_userbase_dir+sep, new_sys)
            log.AppendText("Setup has had to rename your old " + _userbase_dir + "\n")
            log.AppendText("directory, it has been moved to " + new_sys + "\n")
            log.AppendText("So make sure you go check there to see if there is anything in ")
            log.AppendText("that myfiles directory that you need!!\n")
            wx.Yield()
            log.AppendText("Removing old Directories: (this could take a moment)\n\n")
            wx.Yield()
            rmtree(_userbase_dir+sep)
            mkdir(_userbase_dir)
            chdir(_userbase_dir)
            
        log.AppendText("Installing OpenRPG user files to " + dyn_dir + "\n")
        log.AppendText("Fetching OpenRPG runtime Files: (this could take a moment)\n")
        wx.Yield()
        wx.BeginBusyCursor()
        hg.clone(self.ui, 'http://hg.assembla.com/traipse', dest=_userbase_dir)
        self.repo = hg.repository(self.ui, _userbase_dir)
        log.AppendText("\n")
        log.AppendText('Halloween 2009 Edition!!\n')
        log.AppendText('Copying Portable Mercurial to '+_userbase_dir+sep+'upmana\n')
        if exists(_userbase_dir+sep+'upmana'+sep+'mercurial'): 
            rmtree(_userbase_dir+sep+'upmana'+sep+'mercurial')
        copytree(_home+sep+'mercurial', _userbase_dir+sep+'upmana'+sep+'mercurial')
        rmtree(_userbase_dir+sep+'upmana'+sep+'mercurial'+sep+'hgweb')
        copytree(_userbase_dir+sep+'upmana'+sep+'mercurial'+sep+'portable_hgweb', _userbase_dir+sep+'upmana'+sep+'mercurial'+sep+'hgweb')
        rmtree(_userbase_dir+sep+'upmana'+sep+'mercurial'+sep+'portable_hgweb')
        wx.EndBusyCursor()

        #############

        try:
            log.AppendText("\n")
            _user_dir = _userbase_dir + sep + 'myfiles'
            #makedirs(_user_dir) #Removed because Traipse has a myfiles directory in the repo.
            log.AppendText("Creating the myfiles Directory:\n")
            wx.Yield()
            log.AppendText("You should copy your old myfiles directory to this new location\n")
            wx.Yield()
            makedirs(_user_dir + sep + "runlogs" + sep);
            log.AppendText("Creating the runlogs directory\n")
            wx.Yield()
            makedirs(_user_dir + sep + "logs" + sep);
            log.AppendText("Creating the Chat Logs directory\n")
            wx.Yield()
            # makedirs(_user_dir + sep + "webfiles" + sep) # Traipse contains a webfiles folder
            log.AppendText("Creating the Webfiles Directory\n")
            wx.Yield()
        except:
            pass

        log.AppendText("Setting your copy to the Ornery Orc Release. You are invited to modify ")
        log.AppendText("the code. Re-run setup.py if you break it hard.\n\n")
        wx.Yield()
        chdir(_userbase_dir)
        hg.update(self.repo, "ornery-orc")
        log.AppendText('\n')
        wx.Yield()
        log.AppendText("Traipse 'OpenRPG' has been setup, You can now run OpenRPG via one of ")
        log.AppendText("the launcher scripts (Traipse.pyw, Server.py, Server_GUI.py)\n")
        log.AppendText("Do not forget your new myfiles location is " + _user_dir + "\n")
        log.AppendText("You will need to copy your old myfile directory there so that you ")
        log.AppendText("have access to your settings and game trees\n")
        wx.Yield()
        log.AppendText("\n\nDONE! You can close this window now and delete the _del ")
        log.AppendText("directory after you have ensure OpenRPG is running properly")


class SetupApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        self.frame = InstallWindow()
        self.frame.Show()
        return True

app = SetupApp(0)
app.MainLoop()
