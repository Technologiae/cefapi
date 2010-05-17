from cefbase import *

class DiocesesPage(webapp.RequestHandler):
	def get(self):
		diocese = None
		for result in db.GqlQuery("SELECT * FROM Diocese WHERE owner = :1 LIMIT 1", users.get_current_user()):
			diocese = result
		if diocese:
			path = os.path.join(os.path.dirname(__file__), 'dioceses.html')
			self.response.out.write(template.render(path, {'user': users.get_current_user(),
															'diocese': diocese.name,
															'logout_url': users.create_logout_url(self.request.uri)}))
		else:
			Diocese(name="#inconnu#", owner=users.get_current_user()).put()
		
application = webapp.WSGIApplication(
									 [('/dioceses/', DiocesesPage)],
									 debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()