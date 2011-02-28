# le constructeur de la classe Authentification se trouve dans le fichier authentification.py (dans la racine du projet)
from cefbase import *
from authentification import *
from cefbase import *
from google.appengine.api import users

class LinksReorderTask(webapp.RequestHandler):
	def get(self, menu_key):
		user = Authentification.check_authentification()
		if not user:
			self.redirect(users.create_login_url(self.request.uri))		
		else:
			order = map(int, self.request.get('order').split(","))
			menu = Menu.get(menu_key)
			links = sorted(menu.link_set, key=lambda link: link.order)
					
			for i in range(0,len(links)):
				links[order[i]].order = i
	
			db.put(links)
			memcache.flush_all()

class LinksPage(webapp.RequestHandler):
	def post(self, menu_key):
		user = Authentification.check_authentification()
		if not user:
			self.redirect(users.create_login_url(self.request.uri))		
		else:
			menu = Menu.get(menu_key)
			links = sorted(menu.link_set, key=lambda link: link.order)
			if len(links) > 0:
				new_position = max(map(lambda x: x.order, links)) + 1
			else:
				new_position = 0
		
			url = self.request.get('url')
			if not url:
				url = None
			link = Link(
				name = self.request.get('name'),
				url = url,
				order = new_position
			)
		
			link.menu = menu.key()
		
			link.put()	
			memcache.flush_all()
			
			self.redirect('/admin/menus/'+menu_key)	
			
class LinkPage(webapp.RequestHandler):
	def get(self, menu_key, link_key):
		user = Authentification.check_authentification()
		if not user:
			self.redirect(users.create_login_url(self.request.uri))		
		else:
			link = Link.get(link_key)
			
			path = os.path.join(os.path.dirname(__file__), 'templates/link.html')
			self.response.out.write(template.render(path, { 'title': "Editer le lien", 'menu_key': menu_key, 'link': link }))
			
	def put(self, menu_key, link_key):
		user = Authentification.check_authentification()
		if not user:
			self.redirect(users.create_login_url(self.request.uri))		
		else:
			link = Link.get(link_key)
			link.name = self.request.get('name')
			#url = self.request.get('url');
			#if not url:
			url = None
			link.url = url
			link.put()
			memcache.flush_all()
			self.redirect('/admin/menus/'+menu_key)	

	def post(self, menu_key, link_key):	
		if self.request.get('method') == 'put':
			self.put(menu_key, link_key)
	
	def delete(self, menu_key, key):
		user = Authentification.check_authentification()
		if not user:
			self.redirect(users.create_login_url(self.request.uri))		
		else:
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