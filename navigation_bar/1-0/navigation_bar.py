# Templates reference:
# http://www.djangoproject.com/documentation/0.96/templates/

from cefbase import *

import jsmin
jsm = jsmin.JavascriptMinify()

class NavbarScript(webapp.RequestHandler):
	# code correspond au nom du fichier .js (exemple: cef, clermont...)
	def get(self, code):
		if 'Host' in self.request.headers.keys():
			host = self.request.headers['Host']
		else:
			raise NameError('MissingHost')
		
		# Systeme de cache
		js_response = memcache.get(NEW_VALUE_WHEN_DEPLOYED + "_js_response_" + code)
		# Le cache est desactive en local
		if host == "localhost:8080": js_response = None
		
		if js_response is None:
			navbar = Navbar.all().filter("code =", code)[0]
			
			# Options pour defaut
			template_vars = {
				'dioceses_menu_off': False,
				'acces_direct_menu_off': False,
				'ressources_menu_off': False,
				'social_links_off': False,
				'host': host
			}
			
			# On met a jour les options pour que ca corresponde a l instance navbar.settings	
			template_vars.update(dict((setting,True) for setting in navbar.settings))
						
			try:
				nav_links = {
					'cef': sorted(Menu.all().filter("special_kind =", "cef").fetch(1)[0].link_set, key=lambda link: link.order),
					'liturgie': sorted(Menu.all().filter("special_kind =", "liturgie").fetch(1)[0].link_set, key=lambda link: link.order),
					'autres': sorted(Menu.all().filter("special_kind =", "autres").fetch(1)[0].link_set, key=lambda link: link.order),
					'messes': sorted(Menu.all().filter("special_kind =", "messes").fetch(1)[0].link_set, key=lambda link: link.order),
					'eglise_universelle': sorted(Menu.all().filter("special_kind =", "eglise_universelle").fetch(1)[0].link_set, key=lambda link: link.order),
					'annuaire_des_sites': sorted(Menu.all().filter("special_kind =", "annuaire_des_sites").fetch(1)[0].link_set, key=lambda link: link.order),
					'dioceses': sorted(Menu.all().filter("special_kind =", "dioceses").fetch(1)[0].link_set, key=lambda link: link.order),
				}
			except IndexError:
				raise NameError('Un des menus speciaux est manquant en base de donnees... Avez vous initialise les menus ?')		
			
			# A cause des problemes d encodage sous internet explorer, on utilise les "html entities"
			def html_entities(x): return escape(x).encode("ascii", "xmlcharrefreplace")
			
			# Escaping name of links (using html entites)
			for key, category in nav_links.items():
				for link in category:
					link.name = html_entities(link.name)
			
			template_vars['nav_links'] = nav_links
			
			template_vars['first_menu'] = navbar.first_menu
			if template_vars['first_menu']: template_vars['first_menu_links'] = sorted(navbar.first_menu.link_set, key=lambda link: link.order)
			
			template_vars['second_menu'] = navbar.second_menu
			if template_vars['second_menu']: template_vars['second_menu_links'] = sorted(navbar.second_menu.link_set, key=lambda link: link.order)
			
			template_vars['third_menu'] = navbar.third_menu
			if template_vars['third_menu']: template_vars['third_menu_links'] = sorted(navbar.third_menu.link_set, key=lambda link: link.order)
			
			template_vars['fourth_menu'] = navbar.fourth_menu
			if template_vars['fourth_menu']: template_vars['fourth_menu_links'] = sorted(navbar.fourth_menu.link_set, key=lambda link: link.order)
			
			js_template_path = os.path.join(os.path.dirname(__file__), 'navigation_bar.js')
			navbar_template_path = os.path.join(os.path.dirname(__file__), 'navigation_bar.html')
			search_results_template_path = os.path.join(os.path.dirname(__file__), 'search_results.html')
			
			# Rendering and escaping html template
			navbar_template = template.render(navbar_template_path, template_vars).replace('\n', '').replace('\t', '').replace('\"', '\\\"')
			search_results_template = template.render(search_results_template_path, {}).replace('\n', '').replace('\t', '').replace('\"', '\\\"')

			js_template_values = {
				'navbar_template': navbar_template,
				'search_results_template': search_results_template,
				'navbar': navbar,
				'host': host
			}

			js_response = template.render(js_template_path, js_template_values);
			
			## Javascript minified
			output = StringIO.StringIO()
			jsm.minify(StringIO.StringIO(js_response), output)
			js_response = output.getvalue()
			
			# Memcache added (will change on next deployment)
			memcache.add(key=NEW_VALUE_WHEN_DEPLOYED + "_js_response_" + code, value=js_response, time=86400)
		
		self.response.headers['Content-Type'] = 'text/javascript; charset=UTF-8'
		self.response.headers['Cache-Control'] = 'private, max-age=3600, must-revalidate'
		
		self.response.out.write(js_response)		

application = webapp.WSGIApplication(
									 [(r'/api/(.+)\.js', NavbarScript)],
									 debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
