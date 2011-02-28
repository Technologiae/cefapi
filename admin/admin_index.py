#Interface d'accueil de la page d'admin
# permet de selectionner les donnees qu'on envoie selon l'utilisateur 
 
from cefbase import *
from google.appengine.api import users
from authentification import *

class AdminPage(webapp.RequestHandler):
	def get(self):
		user = Authentification.check_authentification()
# on regarde aussi si l'utilisateur est admin app engine		
		url = users.create_logout_url('./')
		url_linktext = 'Deconnexion'
		if not user:
			self.redirect(users.create_login_url(self.request.uri))	
		else:
			if user.admin:
				#L'option admin permet de voire toutes les barres de navigation et tous les menus de tous les contributeurs
				navbars = Navbar.all().order('name').fetch(200)
				menus = Menu.all().order('name').fetch(200)
	 			old_menus = Menu.all().filter("author =", None).filter("shared =", False).order('name').fetch(200)
	 			shared_menus = Menu.all().filter("shared =", True).order('name').fetch(200)
				
			else:
				#Si l'utilisateur est un admin de dioceses:
				#Il ne voit que les barres de menu qu'il a creees
				navbars = Navbar.all().filter("author =",user.user).order('name').fetch(200)
				#Il voit tous les menus qu'il a crees et tous ceux qui ont ete declares commun par un admin
				menus = Menu.all().filter("author =",user.user).order('name').fetch(200)
		 		old_menus = Menu.all().filter("author =", None).filter("shared =", False).order('name').fetch(200)
		 		shared_menus = Menu.all().filter("shared =", True).order('name').fetch(200)
			
			menus_with_navbars = map(lambda menu: {'name': menu.name, 'special_kind': menu.special_kind, 'key': menu.key(),'author': menu.author, 'shared': menu.shared, 'navbar_first_set':menu.navbar_first_set, 'navbar_second_set':menu.navbar_second_set}, menus)
			commun_menus = old_menus
			commun_menus.extend(shared_menus)	
			commun_menus_with_navbars = map(lambda menu: {'name': menu.name, 'special_kind': menu.special_kind, 'key': menu.key(),'author': menu.author, 'shared': menu.shared, 'navbar_first_set':menu.navbar_first_set, 'navbar_second_set':menu.navbar_second_set}, commun_menus)
			
			path = os.path.join(os.path.dirname(__file__), 'templates/admin.html')
			self.response.out.write(template.render(path, {'menus': menus_with_navbars,'commun_menus':commun_menus_with_navbars , 'navbars': navbars,'url': url, 'url_linktext': url_linktext,'user':user}))