import os
import cgi
import datetime
import urllib
import wsgiref.handlers
import base64

from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp.util import run_wsgi_app

import model
import safefilename

PARTSIZE = 9.8 * 1024 * 1024

class AddUpPage(webapp.RequestHandler):

  def get(self, id = None):

    if not users.get_current_user():
	    self.redirect(users.create_login_url(self.request.uri))

    url = users.create_logout_url(self.request.uri)
    url_linktext = 'Logout'

    ### upload_url = blobstore.create_upload_url('')

    if id:
	riff = model.Riff.get_by_id(int(id))
    else:
	riff = False

    template_values = {
    	'ControllerId' : 'upload',
    	'ControllerName' : 'Upload your riff!',
	'InstrumentsList' : model.get_all_musical_instruments(),
	'GenresList' : model.get_all_musical_genres(),
	'url' : url,
	'url_linktext' : url_linktext,
	'riff' : riff,
    }

    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):

    if not users.get_current_user():
	    return


    form = cgi.FieldStorage()    
    id = form['id'].value

    if id == 'none':
	id = None;

    riff_name = form['riffName'].value

    if id:
    	riff = model.Riff.get_by_id(int(id))
	if not riff.author == users.get_current_user():
		return;
    else:
    	riff = model.Riff()

    if len(riff_name) < 4:
      return


    if not id:
	    filelength = len(form['file'].value)
	    firstkey = 0
	    data = form['file'].value
	    this = 0
	    last = None    
	    while this < filelength:
	      if this + PARTSIZE > filelength:
	        next = filelength
	      else:
	        next = this + PARTSIZE
	      uf = model.UploadedFile()
	      part = data[this:next]
	      
	      uf.content = part
	      uf.type = form['file'].type
	      uf.filename = form['file'].filename
	      uf.size = next - this
	      this = next
	      uf.put()
	      if last:
	          last.next = uf
	          last.put()
	      last = uf
	      if firstkey == 0:
	        firstkey = uf.key()    


    riff.author = users.get_current_user()
    riff.name = cgi.escape(riff_name).encode('ascii', 'xmlcharrefreplace')
    riff.genre = form['musicalGenre'].value
    riff.instrument = form['musicalInstrument'].value

    if not id:
    	riff.fileid = firstkey

    riff.put()
    self.redirect('/')
