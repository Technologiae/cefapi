from cefbase import *
from google.appengine.api import users
# Permet de savoir si c'est le bon utilisateur qui cherche a avoir acces aux donnees
# Si l'utlisateur a aucun droit, il n'a acces a rien
# Si le contributeur est un admin de diocese, il n'a acees qu'a ses barres propres, ses menus propres et les menus publics
# Si le contributeur a ete designe admin, il a acces en a toutes les barres de tous les contributeurs et tous les menus. Il peut 
#en plus decider de rendre public ou prive un menu
# Si le contributeur est admin de l'appli elle meme (administrateur app engine), il peut ajouter des contributeurs de diocese et 
#choisir si un contributeur peut avoir acces a l'option admin (acces a toutes les barres et tous les menus)


class Authentification():
    @staticmethod
    def check_authentification(must_admin = False):
        if not users.get_current_user():
            return False
        else:
            list_admin= Administrator.all().filter("user =",users.get_current_user()).fetch(1)
            if len(list_admin) == 0:
                if users.is_current_user_admin():
                    admin = Administrator(user=users.get_current_user(),admin=True)
                    admin.put()
                else:
                    return False
            else :
                admin = list_admin[0]
            admin.super_admin=users.is_current_user_admin()
            if must_admin and not admin.admin:
                return False
            return admin
