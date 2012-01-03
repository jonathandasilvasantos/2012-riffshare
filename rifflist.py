import os
import cgi
import datetime
import urllib
import wsgiref.handlers


from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import model;

class ListAllPage(webapp.RequestHandler):

  def get(self):

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
	    logged = True
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
	    logged = False

	riffs = model.Riff.all().order('-date')

        template_values = {
         'riffs': riffs,
    	'ControllerId' : 'list',
    	'ControllerName' : 'List of riffs',
	'url' : url,
	'url_linktext' : url_linktext,
	'edit' : False,
	'logged' : logged
        }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

class ListMyPage(webapp.RequestHandler):

  def get(self):

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
	    logged = True
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
	    logged = False

	riffs = model.Riff.all().order('-date')

	my = self.request.get('my')


	if not users.get_current_user():
	  self.redirect(url)
	riffs.filter('author =', users.get_current_user())

        template_values = {
         'riffs': riffs,
    	'ControllerId' : 'list',
    	'ControllerName' : 'List of riffs',
	'url' : url,
	'url_linktext' : url_linktext,
	'edit' : True,
	'logged' : logged
        }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))
