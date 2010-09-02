from cefbase import *

class AdminPage(webapp.RequestHandler):
	def get(self):
		path = os.path.join(os.path.dirname(__file__), 'admin.html')
		self.response.out.write(template.render(path, {}))

class NewsLinksPage(webapp.RequestHandler):
	def get(self):
		newsLinks = NewsLink.all().order('order').fetch(15)

		# if users.get_current_user():
		#	 author = users.get_current_user()

		template_values = {
			'newsLinks': newsLinks,
			'title': "Liens d&#x27;actualit&eacute;"
		}

		path = os.path.join(os.path.dirname(__file__), 'newsLinks.html')
		self.response.out.write(template.render(path, template_values))
		
	def post(self):
		new_position = max(map(lambda x: x.order, NewsLink.all().fetch(50))) + 1
		
		newsLink = NewsLink(
			name = self.request.get('name'),
			url = self.request.get('url'),
			order = new_position
		)

		if users.get_current_user():
			 newsLink.author = users.get_current_user()
		
		newsLink.put()	
		memcache.flush_all()
			
		self.redirect('newsLinks')

class NewsLinksReorder(webapp.RequestHandler):
	def get(self):
		order = map(int, self.request.get('order').split(","))
		newsLinks = NewsLink.all().order('order').fetch(50)
		
		for i in range(0,len(newsLinks)):
			newsLinks[order[i]].order = i

		db.put(newsLinks)
		memcache.flush_all()
		
		self.redirect('/admin/newsLinks')

class NewsLinkPage(webapp.RequestHandler):
	def delete(self, key):
		newsLink = NewsLink.get(key)
		newsLink.delete()
		# Reorder other links
		i = 0
		newsLinks = NewsLink.all().order('order').fetch(50)
		for newsLink in newsLinks:
			newsLink.order = i
			newsLink.put()
			i+=1
		db.put(newsLinks)
		# Flush memcache
		memcache.flush_all()
		
		self.redirect('/admin/newsLinks')

application = webapp.WSGIApplication(
									 [('/admin/', AdminPage),
									  ('/admin/newsLinks', NewsLinksPage),
									  ('/admin/newsLinks/reorder', NewsLinksReorder),
									  (r'/admin/newsLinks/(.*)', NewsLinkPage)],
									 debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()