from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.ext import db
import model

class DeleteService(webapp.RequestHandler):
  def get(self, id=None):

	if id:
		riff = model.Riff.get_by_id(int(id))
		if not riff.author == users.get_current_user():
			return;

		all_files = []

		uf = model.UploadedFile.get_by_id(riff.fileid.key().id())

		all_files.append(uf.key().id())

		while True:
			if uf.next:
				uf = uf.next
				all_files.append(uf.key().id())
			else:
				break
		for item in all_files:
			file = model.UploadedFile.get_by_id(item)
			file.delete()
		
		rattings = model.Rate.all()
		rattings.filter('riff =', riff)
		db.delete(rattings)

		riff.delete()
		
 	
