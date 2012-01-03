import os
import datetime
import urllib

from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.api import users
from google.appengine.ext.webapp import blobstore_handlers
import model;

class Rate(db.Model):
  author = db.UserProperty()
  riff = db.ReferenceProperty()

class Riff(db.Model):
  author = db.UserProperty()
  name = db.StringProperty(multiline=False)
  instrument = db.StringProperty(multiline=False)
  genre = db.StringProperty(multiline=False)
  ratting = db.IntegerProperty()
  date = db.DateTimeProperty(auto_now_add=True)
  fileid =  db.ReferenceProperty()
  rates = db.IntegerProperty(default=0)



def get_all_musical_instruments():
  instruments = ['guitar','piano']
  return instruments

def get_all_musical_genres():
  genres = ['blues','rock']
  return genres

class UploadedFile(db.Model):
  content = db.BlobProperty()
  filename = db.StringProperty()
  is_head = db.BooleanProperty()
  size = db.IntegerProperty()
  type = db.StringProperty()
  next = db.ReferenceProperty()



