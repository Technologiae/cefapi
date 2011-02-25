from cefbase import *
from google.appengine.api import users

class Authentification():
    @staticmethod
    def check_authentification(must_admin = False):
        if not users.get_current_user():
            return False
        else:
            list_admin= Administrator.all().filter("user =",users.get_current_user()).fetch(1)
            if len(list_admin) == 0:
                return False
            else:
                admin = list_admin[0]
                if must_admin and not admin.admin:
                    return False
                return admin
