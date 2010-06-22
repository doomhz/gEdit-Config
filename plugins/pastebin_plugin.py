#  Copyright (C) 2009 - Amir Hadzic <amir.hadzic91@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330,
#  Boston, MA 02111-1307, USA.

import gedit
import pastebin
import getpass
import gtk

class DocumentUploader(pastebin.ContentUploader):
    def __init__(self, document, life):
        pastebin.ContentUploader.__init__(self)
        self.document = document
        self.life = life

    def get_syntax(self):
        # TODO: Code a more reliable method for syntax checking
        #       ( look at FileUploader in pastebin.py )
       
        if self.document.get_language():
            return self.document.get_language().get_id()
        else:
            return 'text'
        
    def get_content(self):
        if self.document.get_has_selection():
            selection = self.document.get_selection_bounds()
            return self.document.get_slice(selection[0], selection[1])
        else:
            return self.document.get_property("text")
        
    def get_name(self):
        return getpass.getuser()

ui_str = """<ui>
    <menubar name="MenuBar">
        <menu name="ToolsMenu" action="Tools">
            <placeholder name="ToolsOps_2">
                <menuitem name="Pastebin" action="Pastebin" />
            </placeholder>
        </menu>
    </menubar>
</ui>"""
                
class PastebinPluginInstance(gedit.Plugin):
    def __init__(self, window):
        self.window = window
        self.insert_menu()
        
    def activate(self):
        pass
    
    def deactivate(self):
        pass
        
    def update_ui(self):
        pass
        
    def insert_menu(self):
        manager = self.window.get_ui_manager()
        
        self.action_group = gtk.ActionGroup("PastebinPluginActions")
        self.action_group.add_actions([("Pastebin", None,
                                        _("Send to pastebin"), None,
                                        _("Send the document to pastebin.com"),
                                        self.on_send_activate)])
        manager.insert_action_group(self.action_group, -1)
        self.ui_id = manager.add_ui_from_string(ui_str)

    def remove_menu(self):
        manager = self.window.get_ui_manager()
        
        manager.remove_ui(self.ui_id)
        manager.remove_action_group(self.action_group)
        
        manager.ensure_update()
        
    def update_ui(self):
        self.action_group.set_sensitive(self.window.get_active_document() != None)

    def on_send_activate(self, action):
        doc = self.window.get_active_document()
            
        uploader = DocumentUploader(doc, "m")
        url = uploader.publish()
        
        # Show the url
        md = gtk.MessageDialog(self.window, 
            gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
            gtk.BUTTONS_CLOSE, url)
        md.run()
        md.destroy()
     
        
        
class PastebinPlugin(gedit.Plugin):
    def __init__(self):
        gedit.Plugin.__init__(self)
        self._instances = {}
        
    def activate(self, window):
        self._instances[window] = PastebinPluginInstance(window)

    def deactivate(self, window):
        self._instances[window].deactivate()
        del self._instances[window]

    def update_ui(self, window):
        self._instances[window].update_ui()
