"CEF API" comprend:
- la barre de navigation
- l'interface d'administration
- le site recherche.catholique.fr

====
TECHNOLOGIE & HÉBERGEMENT
====

Ce programme est hébergé sur Google App Engine.
Son identifiant est "catholiquefr"
http://appengine.google.com/dashboard?app_id=catholiquefr

====
INSTALLATION (initialisation)
====

Effectuer l'importation suivante:
/admin/import

Attention ! Cette importation ne doit être effectuée qu'une seule fois !

====
RÉGLAGES
====
Le compte eglise.catholique.france@gmail.com est utilisé pour afficher la liste des moteurs de recherche personnalisés.
Le mot de passe se configure dans le fichier settings.py

====
EMPLACEMENT DU DÉPOT
====

Le dépôt de code se trouve sur le dépôt technologie (http://svn.technologiae.org/svn/)
Pour consulter le dépôt: http://forge.technologiae.org/projects/catholiquefr/repository


====
CORRECTIONS DE BUGS
AMÉLIORATIONS POSSIBLES
====

- Prévoir un système de sauvegardes pour les moteurs de recherche
- Liste des dossiers d'actualité: permettre l'exportation pour utilisation dans l'application iPhone (Attention: ajouter une image et une description !)
- Installer le moteur de recherche sur le site de Soissons
- Corriger bug IE : caractères accentués (Dans les 2 messages d'erreur)
- BUG: (dans le site messesInfo) touche "entrée" pour lancer la recherche
- Contacter Lyon (Jeunes) pour la barre de navigation (ils en ont fait une version spécifique).
- BUG: http://recherche.catholique.fr/?q=gabriel&sites=dioc%E8ses ( (bug non reproduit sur safari et firefox)
correction: si, bug reproduit sur safari en production...)
- Ajout de l'auto-complétion?
- Changer "debug=True" !!!
- SPIP: problème d'affichage des boutons "Modifier rubrique" et "recalculer" avec la barre de navigation





==========
HISTORIQUE
==========

77
22/09/2010 11:44
Ajout de la possibilité de sélectionner directement un moteur de recherche de compte eglise.catholique.france@gmail.com

76
07/09/2010 17:16
Petites corrections

75
07/09/2010 16:11
Ajout de nouvelles fonctionnalités:
édition du nom d'un lien, menu ou barre de navigation

74
07/09/2010 15:04
Reorganisation du dossier admin

73
07/09/2010 14:42
Correction de bugs:
- absence de memecache.flush
- absence de tri dans l'affichage des menus
- correction de style

72
06/09/2010 19:07
Améliorations de l'interface d'administration

71
06/09/2010 11:47
Changement de version (version 2)

70
06/09/2010 11:46
Ajout de Menu, Link et Navbar
Interface d'administration
Script d'importation

69
02/09/2010 16:07
Ajout de la possibilité de réordonner la liste des liens

68
24/08/2010 14:39
Correction de bugs et petites améliorations. (version 1-0-5)

27
28/05/2010 16:54
Possibilité de charger la barre de navigation sans passer par le mode asynchrone.

25
17/05/2010 09:56
Version 1.0.2
Modification des styles de la lightbox de recherche.
Utilisation d'un template pour cette lightbox
Création d'un extranet diocèses (alpha)

24
07/05/2010 12:12
Version 1.0.1
Utilisation d'un module pour regrouper les imports et les classes

23
07/05/2010 11:38
Version 1.0.1
Les liens d'actualité sont désormais stockés en base de données.
Ajout d'une interface d'administration pour ces liens.

22
06/05/2010 16:28
Version 1:
Correction d'un bug lié au cache.

21
05/05/2010 17:20
Passage en version 1.0
- Le mode de chargement asynchrone est désormais obligatoire
- Ajout de commentaires dans le code
- Ajout de deux liens d'actualité
- La barre ne s'affiche pas à l'impression

20
03/05/2010 14:26
Préparation du passage de l'application en version 1.0

18
30/04/2010 11:23
Ajout de cache (côté client) pour le script. Durée 1h.

17
30/04/2010 11:09
Ajout d'une option pour supprimer l'animation
Memcache désactivé en local
La barre ne s'affiche plus avant que les css soient chargés.

16
29/04/2010 22:19
Correction d'un bug avec la lightbox des résultats de recherche.

15
29/04/2010 22:06
Ajout d'une option pour garder la barre de navigation fixe (toujours visible), activée par defaut.
Ajouter "scrolling_bar: false" pour désactiver.

14
29/04/2010 19:53
v0-4-7
Ajout d'une option pour que le chargement de la barre de navigation soit plus rapide.

13
29/04/2010 19:25
Encodage des caractères rendu automatique (e accent aigu devient é)

10
29/04/2010 18:04
Ajout de JSMIN (compression du javascript).

9
29/04/2010 16:48
Ajout de memcache pour le template du fichier JS (navigation_bar).
v0-4-6