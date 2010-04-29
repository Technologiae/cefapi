# Templates reference:
# http://www.djangoproject.com/documentation/0.96/templates/

import cgi
import os
from google.appengine.ext.webapp import template

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class SearchHome(webapp.RequestHandler):
	def get(self):
		query = self.request.get('q').replace('\"', '&quot;').replace('recherche.catholique.fr', '')
		query_escaped = self.request.get('q').replace('\"', '\\\"')
		sites = self.request.get('sites')
		
		html_template_path = os.path.join(os.path.dirname(__file__), 'recherche.html')
		
		html_template_values = {
			'query': query,
			'query_escaped': query_escaped,
			'sites': sites
		}
		
		self.response.out.write(template.render(html_template_path, html_template_values))

application = webapp.WSGIApplication(
									 [('/', SearchHome)],
									 debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
