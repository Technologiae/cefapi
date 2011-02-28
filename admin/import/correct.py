from cefbase import *
from google.appengine.api.users import *

class ImportTask(webapp.RequestHandler):
	def get(self):
		
		navbars = Navbar.all().order('name').fetch(200)
		for navbar in navbars:
			navbar.author=User("eglise.catholique.france@gmail.com")
			navbar.put()
		menus = Menu.all().order('name').fetch(200)
		for menu in menus:
			if not menu.author:	
				menu.author=User("eglise.catholique.france@gmail.com")
				menu.put()
		
		memcache.flush_all()
	
		self.redirect('/admin/')		


application = webapp.WSGIApplication(
									 [('/admin/correct', ImportTask)],
									 debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()