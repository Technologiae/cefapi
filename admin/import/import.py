from cefbase import *
from google.appengine.api.users import *

class ImportTask(webapp.RequestHandler):
	def get(self):
		
		f = open(os.path.join(os.path.dirname(__file__), 'links_init.yaml'))
		links_init = yaml.load(f)
		f.close()
		
		menu_cef = Menu(name=u"Conf. des eveques de France", special_kind="cef", shared=True).put()
		for position, link in enumerate(links_init['cef']):
			Link(name=link['name'], url=link['url'], order=position, menu=menu_cef).put()
		
		menu_liturgie = Menu(name="Liturgie", special_kind="liturgie", shared=True).put()
		for position, link in enumerate(links_init['liturgie']):
			Link(name=link['name'], url=link['url'], order=position, menu=menu_liturgie).put()
			
		menu_messes = Menu(name="Messes", special_kind="messes", shared=True).put()
		for position, link in enumerate(links_init['messes']):
			Link(name=link['name'], url=link['url'], order=position, menu=menu_messes).put()
		
		menu_eglise_universelle = Menu(name=u"Eglise universelle", special_kind="eglise_universelle", shared=True).put()
		for position, link in enumerate(links_init['eglise_universelle']):
			Link(name=link['name'], url=link['url'], order=position, menu=menu_eglise_universelle).put()
			
		menu_annuaire_des_sites = Menu(name="Annuaire des sites", special_kind="annuaire_des_sites", shared=True).put()
		for position, link in enumerate(links_init['annuaire_des_sites']):
			Link(name=link['name'], url=link['url'], order=position, menu=menu_annuaire_des_sites).put()
		
		menu_dioceses = Menu(name=u"Dioceses", special_kind="dioceses", shared=True).put()
		for position, link in enumerate(links_init['dioceses']):
			Link(name=link['name'], url=link['url'], order=position, menu=menu_dioceses).put()
		
		menu_autres = Menu(name="Autres", special_kind="autres", shared=True).put()
		for position, link in enumerate(links_init['autres']):
			Link(name=link['name'], url=link['url'], order=position, menu=menu_autres).put()
				
		menu_catholiquefr = Menu(name="eglise.catholique.fr", shared=True).put()
		for position, link in enumerate(links_init['catholiquefr']):
			Link(name=link['name'], url=link['url'], order=position, menu=menu_catholiquefr).put()
		
		menu_actus = Menu(name = "Dossiers actu", author = users.get_current_user(), shared=True).put()
		
		cef_navbar = Navbar(code = "cef", name = "CEF")
		cef_navbar.first_menu = menu_catholiquefr
		cef_navbar.second_menu = menu_actus
		cef_navbar.put()
		
		memcache.flush_all()
	
		self.redirect('/admin/')		


application = webapp.WSGIApplication(
									 [('/admin/import', ImportTask)],
									 debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()