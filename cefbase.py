import cgi
import os
import yaml
import StringIO

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

from django.utils.html import escape

NEW_VALUE_WHEN_DEPLOYED = os.environ['CURRENT_VERSION_ID']

class NewsLink(db.Model):
	name = db.StringProperty(required=True)
	author = db.UserProperty()
	date = db.DateTimeProperty(auto_now_add=True)
	url = db.LinkProperty(required=True)
	order = db.IntegerProperty(required=True)