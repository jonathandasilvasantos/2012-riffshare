from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp.util import run_wsgi_app
import model

class ProviderPage(webapp.RequestHandler):
  def get(self, id=None):
    if id:
      uf = model.UploadedFile.get_by_id(int(id))
      self.response.headers['Content-disposition'] = 'attechment; filename=%s'% uf.filename 
      self.response.headers['Content-Type'] = uf.type

      self.response.out.write(uf.content)
      while uf.next:
        uf = uf.next
        self.response.out.write(uf.content)

