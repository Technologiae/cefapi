# Templates reference:
# http://www.djangoproject.com/documentation/0.96/templates/

import yaml
import cgi
import os
import jsmin
from google.appengine.ext.webapp import template

import StringIO

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import memcache

NEW_VALUE_WHEN_DEPLOYED = os.environ['CURRENT_VERSION_ID']
jsm = jsmin.JavascriptMinify()

class NavigationBar(webapp.RequestHandler):
	def get(self):
		js_response = memcache.get(NEW_VALUE_WHEN_DEPLOYED + "_js_response")
		if js_response is None:
			if 'Host' in self.request.headers.keys():
				host = self.request.headers['Host']
			else:
				raise NameError('MissingHost')

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

			js_response = template.render(js_template_path, js_template_values);
			
			output = StringIO.StringIO()
			jsm.minify(StringIO.StringIO(js_response), output)
			
			js_response = output.getvalue()
			
			memcache.add(key=NEW_VALUE_WHEN_DEPLOYED + "_js_response", value=js_response, time=86400)
		
		self.response.headers['Content-Type'] = 'text/javascript; charset=UTF-8'
		self.response.out.write(js_response)		

application = webapp.WSGIApplication(
									 [('/api/navigation_bar.0-4.js', NavigationBar)],
									 debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
