import os
import cgi
import datetime
import urllib
import wsgiref.handlers

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import model;
import riffhome
import riffaddup
import rifflist
import riffprovider
import riffdelete
import riffrate

application = webapp.WSGIApplication([
  ('/', riffhome.HomePage),
  ('/addup/([0-9]+)', riffaddup.AddUpPage),
  ('/addup/', riffaddup.AddUpPage),
  ('/upload/.*', riffaddup.AddUpPage),
  ('/list/', rifflist.ListAllPage),
  ('/list/my/.*', rifflist.ListMyPage),
  ('/delete/([0-9]+)', riffdelete.DeleteService),
  ('/provider/([0-9]+)', riffprovider.ProviderPage),
  ('/rate/([0-9]+)/([0-9]+)', riffrate.RateService),
  ('/rpc', riffrate.RPCHandler),
], debug=True)



def main():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()
