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

import urllib2
import urllib
import os
import getpass
from gettext import gettext as _

class ContentUploader:
    def __init__(self, content="", syntax="", name="", life="d"):
        self.content = content
        self.syntax = syntax
        self.name = name
        self.life = life
        
    def get_syntax(self):
        return self.syntax
        
    def get_content(self):
        return self.content
        
    def get_name(self):
        return self.name
    
    # really, get one
    def get_life(self):
        return self.life
        
    def publish(self):
        url = 'http://pastebin.com/pastebin.php'
        postdata = [("paste", "Send"),
                ("format", self.get_syntax()),
                ("code2", self.get_content()),
                ("poster", self.get_name()),
                ("expiry", self.get_life())]
        data = urllib.urlencode(postdata)
        req = urllib2.Request(url)
        resp = urllib2.urlopen(req, data)

        # this is the url of the new post
        return resp.geturl()
        
class FileUploader(ContentUploader):
    def __init__(self, filename, life="d"):
        ContentUploader.__init__(self)
        self.file = filename
        self.life = life
    
    def get_syntax(self):
        #TODO: complete the list
        types = {'.py': 'python',
                 '.c' : 'c',
                 '.h' : 'c',
                 '.hpp': 'cpp',
                 '.cpp': 'cpp',
                 '.sh': 'bash',
                 '.pl': 'perl',
                 '.php': 'php',
                 '.lua': 'lua',
                 '.js': 'javascript',
                 '.java': 'java',
                 '.html': 'html4strict'}

        
        ext = os.path.splitext(self.file.lower())[1]
        if ext in types:
           return types[ext]
        else:
           return 'text'

    def get_content(self):
        return open(self.file, "r").read()

    def get_name(self):
        return getpass.getuser()

if __name__ == "__main__":
    thisFile = FileUploader("pastebin.py")
    print thisFile.publish()
