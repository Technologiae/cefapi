from cefbase import *
from google.appengine.api import users

class AdminPage(webapp.RequestHandler):
	def get(self):
		user = users.get_current_user()

		if not user:
			self.redirect(users.create_login_url(self.request.uri))
#		elif user.email() != "toto@admin.com":
#			self.redirect(users.create_login_url(self.request.uri))
		else:
			url = users.create_logout_url('./')
			url_linktext = 'Deconnexion'
			navbars = Navbar.all().filter("author =",user).order('name').fetch(200)
			menus = Menu.all().filter("author =",user).order('name').fetch(200)
 			old_menus = Menu.all().filter("author =", None).order('name').fetch(200)
			
			menus_with_navbars = map(lambda menu: {'name': menu.name, 'special_kind': menu.special_kind, 'key': menu.key(),'author': menu.author, 'shared': menu.shared, 'navbar_first_set':menu.navbar_first_set, 'navbar_second_set':menu.navbar_second_set}, menus)
			old_menus_with_navbars = map(lambda menu: {'name': menu.name, 'special_kind': menu.special_kind, 'key': menu.key(),'author': menu.author,'shared': True, 'navbar_first_set':menu.navbar_first_set, 'navbar_second_set':menu.navbar_second_set}, old_menus)

			path = os.path.join(os.path.dirname(__file__), 'templates/admin.html')
			self.response.out.write(template.render(path, {'menus': menus_with_navbars,'old_menus': old_menus_with_navbars, 'navbars': navbars,'url': url, 'url_linktext': url_linktext}))

