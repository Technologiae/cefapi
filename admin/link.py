from cefbase import *

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