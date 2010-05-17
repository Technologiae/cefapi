# Templates reference:
# http://www.djangoproject.com/documentation/0.96/templates/

from cefbase import *

import jsmin
jsm = jsmin.JavascriptMinify()

class NavigationBar(webapp.RequestHandler):
	def get(self):
		if 'Host' in self.request.headers.keys():
			host = self.request.headers['Host']
		else:
			raise NameError('MissingHost')
		
		js_response = memcache.get(NEW_VALUE_WHEN_DEPLOYED + "_js_response")
		if host == "localhost:8080": js_response = None
		
		if js_response is None:

			js_template_path = os.path.join(os.path.dirname(__file__), 'navigation_bar.js')
			navigation_bar_template_path = os.path.join(os.path.dirname(__file__), 'navigation_bar.html')
			search_results_template_path = os.path.join(os.path.dirname(__file__), 'search_results.html')

			f = open(os.path.join(os.path.dirname(__file__), 'nav_links.yaml'))
			nav_links = yaml.load(f)
			f.close()			
			
			catholiquefr_actu = []
			for link in NewsLink.all().order('order').fetch(15):
				catholiquefr_actu.append({'name': link.name, 'url': link.url})
			
			nav_links['catholiquefr_actu'] = catholiquefr_actu
			
			def html_entities(x): return escape(x).encode("ascii", "xmlcharrefreplace")
			
			# Escaping name of links (using html entites)
			for key, category in nav_links.items():
				for link in category:
					link['name'] = html_entities(link['name'])
			
			navigation_bar_template_values = {
				'nav_links' : nav_links,
				'host': host
			}
			
			# Rendering and escaping html template
			navigation_bar_template = template.render(navigation_bar_template_path, navigation_bar_template_values).replace('\n', '').replace('\t', '').replace('\"', '\\\"')
			search_results_template = template.render(search_results_template_path, {}).replace('\n', '').replace('\t', '').replace('\"', '\\\"')

			js_template_values = {
				'navigation_bar_template': navigation_bar_template,
				'search_results_template': search_results_template,
				'host': host
			}

			js_response = template.render(js_template_path, js_template_values);
			
			# Javascript minified
			output = StringIO.StringIO()
			jsm.minify(StringIO.StringIO(js_response), output)
			js_response = output.getvalue()
			
			# Memcache added (will change on next deployment)
			memcache.add(key=NEW_VALUE_WHEN_DEPLOYED + "_js_response", value=js_response, time=86400)
		
		self.response.headers['Content-Type'] = 'text/javascript; charset=UTF-8'
		self.response.headers['Cache-Control'] = 'private, max-age=3600, must-revalidate'
		
		self.response.out.write(js_response)		

application = webapp.WSGIApplication(
									 [('/api/cef.js', NavigationBar)],
									 debug=False)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
