#Speaks the active file using espeak.

#as of 28-10-07 should support some other languages apart from English,yay!!



#Also stops the speech.



#mainly copied from the example plugin on the gedit website

#please put the files in /usr/lib/gedit-2/plugins/speakit

#TO DO
#make the menu item change when language is changed.
#split the document up into sections if there are different languages
#perhaps add some options into a popup window or something

#BUGS
 #keeps speaking when gedit exits,lol


import gedit
 
import gtk
import os
import subprocess

# Menu item example, insert a new item in the Tools menu
ui_str = """<ui>
<menubar name="MenuBar">
	<menu name="ToolsMenu" action="Tools">
	<placeholder name="ToolsOps_2">
		<menuitem name="Speak" action="SpeakAction"/>
	</placeholder>
	</menu>
</menubar>
</ui>
"""
class ExamplePyWindowHelper:
	def __init__(self, plugin, window):
		self._window = window
		self._plugin = plugin
		self.pid=0
        	self.espeakLanguages=("en","en-sc","en-r","en-n","en-rp","en-wm","af","cs","de","el","eo","es","fi","fr","hr","hu","it","pt","pt-pt","ro","sk","sv","sw")#using the better supported languages on 28-10-07

		# Insert menu items
		self._insert_menu()

	def __del__(self):
		self.stopSpeech() #wtf why doesnt this work??????????????????


	def deactivate(self):
		# Remove any installed menu items
		self._remove_menu()
#		self.stopSpeech()
		self._window = None
		self._plugin = None
		self._action_group = None

	def _insert_menu(self):
		# Get the GtkUIManager
		manager = self._window.get_ui_manager()

		# Create a new action group
		self._action_group = gtk.ActionGroup("Speak")
		self._action_group.add_actions([("SpeakAction", None, _("Toggle Speech"),
										None, _("Stop reading"),
										self.on_toggleSpeech)])

		# Insert the action group
		manager.insert_action_group(self._action_group, -1)



		# Merge the UI
		self._ui_id = manager.add_ui_from_string(ui_str)

	def _remove_menu(self):
		# Get the GtkUIManager
		manager = self._window.get_ui_manager()

		# Remove the ui
		manager.remove_ui(self._ui_id)

		# Remove the action group
		manager.remove_action_group(self._action_group)

		# Make sure the manager updates
		manager.ensure_update()

	def update_ui(self):
		self._action_group.set_sensitive(self._window.get_active_document() != None)


	# Menu activate handlers
	def on_toggleSpeech(self, action):

#		doc = self._window.get_active_document()
		view = self._window.get_active_view()
		buf=view.get_buffer()
		pangoLanguage=buf.get_start_iter().get_language().to_string()#assume same language for whole document 
		self.languageCode="en"#default language is English
		if pangoLanguage in self.espeakLanguages:
			self.languageCode=pangoLanguage
		elif pangoLanguage[0:2] in self.espeakLanguages:
			self.languageCode=pangoLanguage[0:2]
		self.text=buf.get_text(buf.get_start_iter(),buf.get_end_iter())#grab the whole document
		if(not self.pid):#Speech has not been started
			self.startSpeech()
		elif self.speechProcess.poll()==None:#speech has been started and still going
			self.stopSpeech()
		else:#speech has been started but has now finished on its own
			self.startSpeech()

	def stopSpeech(self):
		killall=subprocess.Popen(["killall","espeak"])
		killall.wait()
		self.pid=0

	def startSpeech(self):#launch espeak which does the hard part and speaks the document
		self.stopSpeech()#stop any running espeak processes first
		self.speechProcess=subprocess.Popen(["espeak","-v",self.languageCode,self.text])
		self.pid = self.speechProcess.pid

		
class speakit(gedit.Plugin):
    def __init__(self):
        gedit.Plugin.__init__(self)
        self._instances = {}

    def activate(self, window):
        self._instances[window] = ExamplePyWindowHelper(self, window)

    def deactivate(self, window):
        self._instances[window].deactivate()
        del self._instances[window]
    def update_ui(self, window):
        self._instances[window].update_ui()

