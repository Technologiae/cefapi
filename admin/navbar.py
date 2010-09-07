from cefbase import *
import random

class NavbarPage(webapp.RequestHandler):
	def get(self, navbar_key):
		navbar = Navbar.get(navbar_key)
		menus = Menu.all().order("name").fetch(200)
		menus = list(menu for menu in menus if menu.special_kind == None) # Supprime les menus speciaux de la liste
		menus_list = map(lambda menu: {'name': menu.name, 'key': menu.key(), 'navbar_first_set':menu.navbar_first_set, 'navbar_second_set':menu.navbar_second_set}, menus)

		template_values = {
			'navbar': navbar,
			'random': random.randint(0,10000000000),
			'menus_list': menus_list,
			'host': self.request.headers['Host']
		}

		path = os.path.join(os.path.dirname(__file__), 'templates/navbar.html')
		
		self.response.out.write(template.render(path, template_values))
	
	def post(self, navbar_key):
		if self.request.get('method') == "put": self.put(navbar_key); return # pour palier a l'absence de la methode PUT des formulaires HTML, on utilise POST
	
	def put(self, navbar_key):
		navbar = Navbar.get(navbar_key)
		
		if self.request.get('first_menu') == "None":
			navbar.first_menu = None
		else:
			navbar.first_menu = Menu.get(self.request.get('first_menu'))
		
		if self.request.get('second_menu') == "None":
			navbar.second_menu = None
		else:
			navbar.second_menu = Menu.get(self.request.get('second_menu'))
		
		navbar.settings = self.request.get('settings', allow_multiple = True)
		
		navbar.put()
		memcache.flush_all()

		self.redirect("")
	
	def delete(self, navbar_key):
		navbar = Navbar.get(navbar_key)
		navbar.delete()
		# Flush memcache
		memcache.flush_all()
		
		self.response.out.write("La barre de navigation a ete supprimee avec succes !")

class NavbarInstructionsPage(webapp.RequestHandler):
	def get(self, navbar_key):
		navbar = Navbar.get(navbar_key)
		path = os.path.join(os.path.dirname(__file__), 'templates/navbar_instructions.html')
		self.response.out.write(template.render(path, {'navbar': navbar, 'title': 'instructions'}))

class NavbarsPage(webapp.RequestHandler):
	def get(self):
		self.redirect("/admin/")
		
	def post(self):
		code = self.request.get('code')
		name = self.request.get('name')
		navbar = Navbar(name= name, code= code).put()
		
		memcache.flush_all()
		self.redirect("/admin/navbars/%s" % navbar)
