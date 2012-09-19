# le constructeur de la classe Menu se trouve dans le fichier cefbase.py (dans la racine du projet)
# le constructeur de la classe Authentification se trouve dans le fichier authentification.py (dans la racine du projet)
from cefbase import *
from authentification import *
from cefbase import *
from google.appengine.api import users

class MenuPage(webapp.RequestHandler):
	def get(self, menu_key):
		menu = Menu.get(menu_key)
		user = Authentification.check_authentification()
		if not user:
			self.redirect(users.create_login_url(self.request.uri))		
		else:
			if not user.admin :
				if menu.author:
					if not user.user==menu.author:
						self.redirect('/admin/')
						return	
				else:
					self.redirect('/admin/')
					return	
			links = sorted(menu.link_set, key=lambda link: link.order)
	
			template_values = {
				'links': links,
				'navbar_first_set': menu.navbar_first_set,
				'navbar_second_set': menu.navbar_second_set,
				'navbar_third_set': menu.navbar_third_set,
				'navbar_fourth_set': menu.navbar_fourth_set,
				'menu': menu,
				'user': user,
			}
			path = os.path.join(os.path.dirname(__file__), 'templates/menu.html')
			self.response.out.write(template.render(path, template_values))
	
	def put(self, menu_key):
		menu = Menu.get(menu_key)
		#Seul le super admin choisi si le menu est commun a tous les admins ou non
		user = Authentification.check_authentification()
		if not user:
			self.redirect(users.create_login_url(self.request.uri))		
		else:
			if user.admin:
				if self.request.get('shared'):	
					if self.request.get('shared')=="true":
						menu.shared = True
						menu.author = None
					else:
						menu.shared = False
						menu.author = user.user
				if self.request.get('name'):
					menu.name = self.request.get('name')
				menu.put()			
				memcache.flush_all()	
			else:
				if menu.author:
					if menu.author== user.user:
						if self.request.get('name'):
							menu.name = self.request.get('name')
						menu.put()			
						memcache.flush_all()
			self.redirect('/admin/menus/'+menu_key)	

	def post(self, menu_key):	
		if self.request.get('method') == 'put':
			self.put(menu_key)
	
	def delete(self, menu_key):
		menu = Menu.get(menu_key)
		user = Authentification.check_authentification()
		if not user:
			self.redirect(users.create_login_url(self.request.uri))		
		else:
			if len(menu.navbar_first_set.fetch(1))>0 or len(menu.navbar_second_set.fetch(1))>0:
				self.response.out.write("Supprimez d'abord les barres de navigation qui utilisent ce menu.")
			else:
				# First delete the links
				for link in menu.link_set:
					link.delete()
				# delete the menu
				menu.delete()
				# Flush memcache
				memcache.flush_all()
				
				self.response.out.write("Le menu et ses liens ont ete supprimes avec succes !")
		
class MenusPage(webapp.RequestHandler):
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
			name = self.request.get('name')
			shared = self.request.get('shared')
			author = users.get_current_user()	
			menu = Menu(name= name, author= author)
			menu_key= menu.put()
	
			if self.request.get('navbar_first_key'):
				navbar = Navbar.get(self.request.get('navbar_first_key'))
				navbar.first_menu = menu
				navbar.put()
			
			if self.request.get('navbar_second_key'):
				navbar = Navbar.get(self.request.get('navbar_second_key'))
				navbar.second_menu = menu
				navbar.put()
			
			if self.request.get('navbar_third_key'):
				navbar = Navbar.get(self.request.get('navbar_third_key'))
				navbar.third_menu = menu
				navbar.put()
			
			if self.request.get('navbar_fourth_key'):
				navbar = Navbar.get(self.request.get('navbar_fourth_key'))
				navbar.fourth_menu = menu
				navbar.put()
			
			memcache.flush_all()
			self.redirect("/admin/menus/%s" % menu_key)