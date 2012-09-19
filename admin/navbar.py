# le constructeur de la classe Navbar se trouve dans le fichier cefbase.py (dans la racine du projet)
# le constructeur de la classe Authentification se trouve dans le fichier authentification.py (dans la racine du projet)
from admin_classes import *
from authentification import *
import random
from cefbase import *
from google.appengine.api import users

class NavbarPage(webapp.RequestHandler):
	def get(self, navbar_key):
		user = Authentification.check_authentification()
		if not user:
			self.redirect(users.create_login_url(self.request.uri))		
		else:
			navbar = Navbar.get(navbar_key)
			menus = Menu.all().filter("author =",user.user).order("name").fetch(200)
			menus = list(menu for menu in menus if menu.special_kind == None) # Supprime les menus speciaux de la liste
			menus_list = map(lambda menu: {'name': menu.name, 'key': menu.key(), 'navbar_first_set':menu.navbar_first_set, 'navbar_second_set':menu.navbar_second_set, 'navbar_third_set':menu.navbar_third_set, 'navbar_fourth_set':menu.navbar_fourth_set}, menus)
			commun_menus = Menu.all().filter("shared =", True).order("name").fetch(200)
			commun_menus.extend(Menu.all().filter("author =", None).filter("shared =", False).order("name").fetch(200))
			commun_menus_list = map(lambda menu: {'name': menu.name, 'key': menu.key(),'shared': menu.shared, 'navbar_first_set':menu.navbar_first_set, 'navbar_second_set':menu.navbar_second_set}, commun_menus)
			
			# Liste des moteurs de recherche disponibles
			gdatafeed = GdataFeed("http://www.google.com/cse/api/default/cse/")
			self.response.out.write(gdatafeed)
			searchengines = map(lambda se: SearchEngineFromXml(se), gdatafeed.elements("CustomSearchEngine"))
			
			template_values = {
				'navbar': navbar,
				'searchengines': searchengines,
				'random': random.randint(0,10000000000),
				'menus_list': menus_list,
				'commun_menus_list': commun_menus_list,
			}
	
			path = os.path.join(os.path.dirname(__file__), 'templates/navbar.html')
			
			self.response.out.write(template.render(path, template_values))
	
	def post(self, navbar_key):
		if self.request.get('method') == "put":
			self.put(navbar_key)  # pour palier a l'absence de la methode PUT des formulaires HTML, on utilise POST
			return
		else:
			self.error(404) # file not found
			return
	
	def put(self, navbar_key):
		user = Authentification.check_authentification()
		if not user:
			self.redirect(users.create_login_url(self.request.uri))		
		else:
			navbar = Navbar.get(navbar_key)
			# Formulaire de changement de nom
			if self.request.get('name') and self.request.get('code'):
				navbar.name = self.request.get('name')
				navbar.code = self.request.get('code')
			# Formulaire pour les options
			elif self.request.get('first_menu') and self.request.get('second_menu') and self.request.get('third_menu') and self.request.get('fourth_menu'):
				if self.request.get('first_menu') == "None":
					navbar.first_menu = None
				else:
					navbar.first_menu = Menu.get(self.request.get('first_menu'))
			
				if self.request.get('second_menu') == "None":
					navbar.second_menu = None
				else:
					navbar.second_menu = Menu.get(self.request.get('second_menu'))
					
				if self.request.get('third_menu') == "None":
					navbar.third_menu = None
				else:
					navbar.third_menu = Menu.get(self.request.get('third_menu'))
				
				if self.request.get('fourth_menu') == "None":
					navbar.fourth_menu = None
				else:
					navbar.fourth_menu = Menu.get(self.request.get('fourth_menu'))
				
				if self.request.get('cse_unique_id') == "this_site":
					navbar.cse_unique_id = None
				elif self.request.get('cse_unique_id') == "other":
					navbar.cse_unique_id = self.request.get('cse_unique_id_other')
				else:
					navbar.cse_unique_id = self.request.get('cse_unique_id')
					
				
				navbar.settings = self.request.get('settings', allow_multiple = True)
			else:
				self.error(404) # file not found
				return
			
			navbar.put()
			memcache.flush_all()
	
			self.redirect("")
	
	def delete(self, navbar_key):
		user = Authentification.check_authentification()
		if not user:
			self.redirect(users.create_login_url(self.request.uri))		
		else:
			navbar = Navbar.get(navbar_key)
			navbar.delete()
			# Flush memcache
			memcache.flush_all()
			
			self.response.out.write("La barre de navigation a ete supprimee avec succes !")

class NavbarInstructionsPage(webapp.RequestHandler):
	def get(self, navbar_key):
		user = Authentification.check_authentification()
		if not user:
			self.redirect(users.create_login_url(self.request.uri))		
		else:
			navbar = Navbar.get(navbar_key)
			path = os.path.join(os.path.dirname(__file__), 'templates/navbar_instructions.html')
			self.response.out.write(template.render(path, {'navbar': navbar, 'title': 'instructions', 'host': self.request.headers['Host']}))

class NavbarsPage(webapp.RequestHandler):
	def get(self):
		user = Authentification.check_authentification()
		if not user:
			self.redirect(users.create_login_url(self.request.uri))		
		else:
			self.redirect("/admin/")
		
	def post(self):
		user = Authentification.check_authentification()
		if not user:
			self.redirect(users.create_login_url(self.request.uri))		
		else:
			code = self.request.get('code')
			name = self.request.get('name')
			author = users.get_current_user()
			navbar = Navbar(name= name, code= code, author= author).put()
			
			memcache.flush_all()
			self.redirect("/admin/navbars/%s" % navbar)
