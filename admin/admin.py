from cefbase import *

class AdminPage(webapp.RequestHandler):
	def get(self):
		navbars = Navbar.all().order('name').fetch(200)
		menus = Menu.all().order('name').fetch(200)
		menus_with_navbars = map(lambda menu: {'name': menu.name, 'special_kind': menu.special_kind, 'key': menu.key(), 'navbar_first_set':menu.navbar_first_set, 'navbar_second_set':menu.navbar_second_set}, menus)
		
		path = os.path.join(os.path.dirname(__file__), 'admin.html')
		self.response.out.write(template.render(path, {'menus': menus_with_navbars, 'navbars': navbars}))
		
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

		path = os.path.join(os.path.dirname(__file__), 'menu.html')
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

class MenuReorder(webapp.RequestHandler):
	def get(self, menu_key):
		order = map(int, self.request.get('order').split(","))
		menu = Menu.get(menu_key)
		links = sorted(menu.link_set, key=lambda link: link.order)
				
		for i in range(0,len(links)):
			links[order[i]].order = i

		db.put(links)
		memcache.flush_all()
		
class LinkPage(webapp.RequestHandler):
	def post(self, menu_key, key):
		menu = Menu.get(menu_key)
		links = sorted(menu.link_set, key=lambda link: link.order)
		if len(links) > 0:
			new_position = max(map(lambda x: x.order, links)) + 1
		else:
			new_position = 0
		
		link = Link(
			name = self.request.get('name'),
			url = self.request.get('url'),
			order = new_position
		)
		
		link.menu = menu.key()
		
		link.put()	
		memcache.flush_all()
			
		self.redirect('/admin/menus/'+menu_key)		
	
	def delete(self, menu_key, key):
		menu = Menu.get(menu_key)
		link = Link.get(key)
		link.delete()
		# Reorder other links
		i = 0
		links = sorted(menu.link_set, key=lambda link: link.order)
		for link in links:
			link.order = i
			link.put()
			i+=1
		db.put(links)
		# Flush memcache
		memcache.flush_all()
	
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
		
application = webapp.WSGIApplication(
									 [('/admin/', AdminPage),
									  ('/admin/menus/', MenusPage),
									  (r'/admin/menus/(.+)/reorder', MenuReorder),
									  (r'/admin/menus/(.+)/links/(.*)', LinkPage),
									  (r'/admin/menus/(.+)', MenuPage)],
									 debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()