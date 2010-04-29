# Templates reference:
# http://www.djangoproject.com/documentation/0.96/templates/

import yaml
import cgi
import os
from google.appengine.ext.webapp import template

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class NavigationBar(webapp.RequestHandler):
	def get(self):
		sourceUrl = ""; host = ""
		
		hkeys = self.request.headers.keys()
		if 'Referer' in hkeys: sourceUrl=self.request.headers['Referer']
		if 'Host' in hkeys: host=self.request.headers['Host']
		
		js_template_path = os.path.join(os.path.dirname(__file__), 'navigation_bar.js')
		html_template_path = os.path.join(os.path.dirname(__file__), 'navigation_bar.html')
		
		f = open(os.path.join(os.path.dirname(__file__), 'nav_links.yaml'))
		nav_links = yaml.load(f)
		f.close()
		
		html_template_values = {
			'nav_links' : nav_links,
			'host': host
		}
		
		html_template = template.render(html_template_path, html_template_values).replace('\n', '').replace('\t', '').replace('\"', '\\\"')
		
		js_template_values = {
			'navigation_bar_template': html_template,
			'host': host
		}
		
		self.response.headers['Content-Type'] = 'text/javascript; charset=UTF-8'
		self.response.out.write(template.render(js_template_path, js_template_values))

application = webapp.WSGIApplication(
									 [('/api/navigation_bar.0-4.js', NavigationBar)],
									 debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
