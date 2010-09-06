from cefbase import *
import random

class NavbarPage(webapp.RequestHandler):
	def get(self, navbar_key):
		navbar = Navbar.get(navbar_key)

		template_values = {
			'navbar': navbar,
			'random': random.randint(0,10000000000),
			'menus_list': Menu.all().order("name").fetch(200)
		}

		path = os.path.join(os.path.dirname(__file__), 'navbar.html')
		self.response.out.write(template.render(path, template_values))
	
	def post(self, navbar_key):
		if self.request.get('method') == "put": self.put(navbar_key); return # pour palier à l'absence de la methode PUT des formulaires HTML, on utilise POST
	
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
		navbar.put()
		
		self.redirect("")
	
	def delete(self, navbar_key):
		navbar = Navbar.get(navbar_key)
		navbar.delete()
		# Flush memcache
		memcache.flush_all()
		
		self.response.out.write("La barre de navigation a été supprimée avec succès !")

class NavbarInstructionsPage(webapp.RequestHandler):
	def get(self, navbar_key):
		navbar = Navbar.get(navbar_key)
		path = os.path.join(os.path.dirname(__file__), 'navbar_instructions.html')
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
		                            
		
application = webapp.WSGIApplication(
									 [(r'/admin/navbars/(.+)/instructions', NavbarInstructionsPage),
									  (r'/admin/navbars/(.+)', NavbarPage),
									('/admin/navbars/', NavbarsPage)],
									 debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()