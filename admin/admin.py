import cgi
import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

class NewsLink(db.Model):
	name = db.StringProperty(required=True)
	author = db.UserProperty()
	date = db.DateTimeProperty(auto_now_add=True)
	url = db.LinkProperty(required=True)
	order = db.IntegerProperty(required=True)

class AdminPage(webapp.RequestHandler):
	def get(self):
		path = os.path.join(os.path.dirname(__file__), 'admin.html')
		self.response.out.write(template.render(path, {}))

class NewsLinksPage(webapp.RequestHandler):
	def get(self):
		newsLinks = NewsLink.all().order('order').fetch(15)

		# if users.get_current_user():
		#	 author = users.get_current_user()

		template_values = {
			'newsLinks': newsLinks,
			'title': "Liens d&#x27;actualit&eacute;"
		}

		path = os.path.join(os.path.dirname(__file__), 'newsLinks.html')
		self.response.out.write(template.render(path, template_values))
		
	def post(self):
		newsLink = NewsLink(
			name = self.request.get('name'),
			url = self.request.get('url'),
			order = int(self.request.get('order'))
		)

		if users.get_current_user():
			 newsLink.author = users.get_current_user()
		
		newsLink.put()	
		memcache.flush_all()
			
		self.redirect('newsLinks')

class NewsLinkPage(webapp.RequestHandler):
	def delete(self, key):
		newsLink = NewsLink.get(key)
		newsLink.delete()
		memcache.flush_all()
		
		self.redirect('/admin/newsLinks')

application = webapp.WSGIApplication(
									 [('/admin/', AdminPage),
									  ('/admin/newsLinks', NewsLinksPage),
									  (r'/admin/newsLinks/(.*)', NewsLinkPage)],
									 debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()