from cefbase import *

class MenuPage(webapp.RequestHandler):
	def get(self, menu_key):
		menu = Menu.get(menu_key)
		links = sorted(menu.link_set, key=lambda link: link.order)

		template_values = {
			'links': links,
			'navbar_first_set': menu.navbar_first_set,
			'navbar_second_set': menu.navbar_second_set,
			'title': "Menu \""+menu.name+"\"",
			'menu_key': menu_key
		}

		path = os.path.join(os.path.dirname(__file__), 'templates/menu.html')
		self.response.out.write(template.render(path, template_values))

	def delete(self, menu_key):
		menu = Menu.get(menu_key)
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
		self.redirect("/admin/")
		
	def post(self):
		name = self.request.get('name')			
		menu = Menu(name= name)
		menu_key= menu.put()
		
		if self.request.get('navbar_first_key'):
			navbar = Navbar.get(self.request.get('navbar_first_key'))
			navbar.first_menu = menu
			navbar.put()
		
		if self.request.get('navbar_second_key'):
			navbar = Navbar.get(self.request.get('navbar_second_key'))
			navbar.second_menu = menu
			navbar.put()
		
		memcache.flush_all()
		self.redirect("/admin/menus/%s" % menu_key)