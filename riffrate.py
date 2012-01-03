from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.ext import db
from django.utils import simplejson
import model

class RateService(webapp.RequestHandler):

  def doRate(self, id=None, stars=None):

	if not users.get_current_user():
		return -1

	if not id or not stars or int(stars) > 5 or int(stars) < 1:
		return -1

	riff = model.Riff.get_by_id(int(id))
	rattings = model.Rate.all()
	rattings.filter('author =', users.get_current_user())
	rattings.filter('riff =', riff)
	
	if rattings.count() > 0:
		return -1

	newrate = model.Rate()
	newrate.author = users.get_current_user()
	newrate.riff = riff.key()
	newrate.put()

	riff.rates = int(riff.rates) + int(stars)
	riff.put()
	return id


  def get(self, id=None, stars=None):

	self.doRate(id, stars)

	self.redirect('/')


class RPCHandler(webapp.RequestHandler):
    """ Allows the functions defined in the RPCMethods class to be RPCed."""
    def __init__(self):
        webapp.RequestHandler.__init__(self)
        self.methods = RPCMethods()

    def get(self):
        func = None

        action = self.request.get('action')
        if action:
            if action[0] == '_':
                self.error(403) # access denied
                return
            else:
                func = getattr(self.methods, action, None)

        if not func:
            self.error(404) # file not found
            return

        args = ()
        while True:
            key = 'arg%d' % len(args)
            val = self.request.get(key)
            if val:
                args += (simplejson.loads(val),)
            else:
                break
        result = func(*args)
        self.response.out.write(simplejson.dumps(result))


class RPCMethods:

    def Rate(self, *args):

	id = args[0]
	stars = args[1]

	if not users.get_current_user():
		return -1

	if not id or not stars or int(stars) > 5 or int(stars) < 1:
		return -1

	riff = model.Riff.get_by_id(int(id))
	rattings = model.Rate.all()
	rattings.filter('author =', users.get_current_user())
	rattings.filter('riff =', riff)
	
	if rattings.count() > 0:
		return id

	newrate = model.Rate()
	newrate.author = users.get_current_user()
	newrate.riff = riff.key()
	newrate.put()

	riff.rates = int(riff.rates) + int(stars)
	riff.put()
	return id

