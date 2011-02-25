from cefbase import *
from google.appengine.api.users import *

class AdministratorsPage(webapp.RequestHandler):
    def get(self):
   
        if users.is_current_user_admin():
            administrators = Administrator.all().fetch(200);
            template_values = {
                 'administrators': administrators,
            }
        
            path = os.path.join(os.path.dirname(__file__), 'templates/administrator.html')
                
            self.response.out.write(template.render(path, template_values))
        else:
            self.redirect("/admin/")
        
    def post(self):

         user = User(self.request.get('email'))
         admin = bool(self.request.get('admin'))
         administrator = Administrator(user=user, admin=admin).put()
         self.redirect("/admin/administrators")

    def delete(self, administrator_key):
        if not users.is_current_user_admin():
            self.redirect("/admin/")        
        else:
            administrator = Administrator.get(administrator_key)
            administrator.delete()
            # Flush memcache
            memcache.flush_all()
            
            self.response.out.write("Le contributeur a ete supprime avec succes !")
 
