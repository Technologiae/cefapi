from cefbase import *

from admin.navbar import *
from admin.menu import *
from admin.link import *

class AdminPage(webapp.RequestHandler):
	def get(self):
		navbars = Navbar.all().order('name').fetch(200)
		menus = Menu.all().order('name').fetch(200)
		menus_with_navbars = map(lambda menu: {'name': menu.name, 'special_kind': menu.special_kind, 'key': menu.key(), 'navbar_first_set':menu.navbar_first_set, 'navbar_second_set':menu.navbar_second_set}, menus)
		
		path = os.path.join(os.path.dirname(__file__), 'templates/admin.html')
		self.response.out.write(template.render(path, {'menus': menus_with_navbars, 'navbars': navbars}))
		
		
application = webapp.WSGIApplication([
									('/admin', AdminPage),
									('/admin/', AdminPage),
									(r'/admin/menus/(.+)/reorder', LinksReorderTask),
									(r'/admin/menus/(.+)/links/', LinksPage),
									(r'/admin/menus/(.+)/links/(.+)', LinkPage),
									(r'/admin/menus/(.+)', MenuPage),
									('/admin/menus/', MenusPage),
									('/admin/navbars/', NavbarsPage),
									(r'/admin/navbars/(.+)/instructions', NavbarInstructionsPage),
									(r'/admin/navbars/(.+)', NavbarPage),
									  ], debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()