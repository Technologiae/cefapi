from cefbase import *

class AdminPage(webapp.RequestHandler):
	def get(self):
		navbars = Navbar.all().order('name').fetch(200)
		menus = Menu.all().order('name').fetch(200)
		menus_with_navbars = map(lambda menu: {'name': menu.name, 'special_kind': menu.special_kind, 'key': menu.key(), 'navbar_first_set':menu.navbar_first_set, 'navbar_second_set':menu.navbar_second_set}, menus)
		
		path = os.path.join(os.path.dirname(__file__), 'templates/admin.html')
		self.response.out.write(template.render(path, {'menus': menus_with_navbars, 'navbars': navbars}))
		