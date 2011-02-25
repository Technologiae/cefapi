from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from admin.admin_classes import *


from admin.navbar import *
from admin.menu import *
from admin.link import *
from admin.searchengine import *
from admin.admin_index import *
from admin.administrator import *
from authentification import *
         
application = webapp.WSGIApplication([
									('/admin', AdminPage),
									('/admin/', AdminPage),
                                    ('/admin/administrators', AdministratorsPage),
                                    (r'/admin/administrators/(.+)', AdministratorsPage),
									(r'/admin/menus/(.+)/reorder', LinksReorderTask),
									(r'/admin/menus/(.+)/links/', LinksPage),
									(r'/admin/menus/(.+)/links/(.+)', LinkPage),
									(r'/admin/menus/(.+)', MenuPage),
									('/admin/menus/', MenusPage),
									('/admin/navbars/', NavbarsPage),
									(r'/admin/navbars/(.+)/instructions', NavbarInstructionsPage),
									(r'/admin/navbars/(.+)', NavbarPage),
									('/admin/searchengines/', SearchenginesPage),
									(r'/admin/searchengines/(.+)', SearchenginePage),
									  ], debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()