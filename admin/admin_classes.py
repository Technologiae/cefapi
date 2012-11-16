from cefbase import *

import xml.dom.minidom
import atom.url
import gdata.service
import gdata.alt.appengine

from settings import *

# Admin-specific classes
class GdataFeed():
	def __init__(self, feed_url):
		# Initialize a client to talk to Google Data API services. 
		# http://gdata-python-client.googlecode.com/svn/trunk/pydocs/gdata.service.html#GDataService
		client = gdata.service.GDataService()
		# Tell the client that we are running in single user mode, and it should not
		# automatically try to associate the token with the current user then store
		# it in the datastore.
		gdata.alt.appengine.run_on_appengine(client, store_tokens=False, single_user_mode=True)
		client.email = CSE_EMAIL
		client.password = CSE_PASSWORD
		# To request a ClientLogin token you must specify the desired service using
		# its service name ("cprose" pour GOOGLE CUSTOM SEARCH)
		client.service = 'cprose'
		# Request a ClientLogin token, which will be placed in the client's
		# current_token member.
		client.ProgrammaticLogin()
		
		self.response = client.Get(feed_url)
		
		encoded_response = unicode(self.response, errors="ignore")
		self.dom = xml.dom.minidom.parseString(encoded_response)
	
	def root_element(self):
		return self.dom.documentElement
	
	def elements(self, tag_name):
		return self.dom.documentElement.getElementsByTagName(tag_name)


# <CustomSearchEngines>
# 	<CustomSearchEngine id="catholique_1" creator="002848703620547974985" title="Nouveau moteur" description="Recherche sur des sites de l'Eglise (test 1)" language="fr"/>
# 	<CustomSearchEngine id="uqc3tjf5wbs" creator="002848703620547974985" title="recherche.catholique.fr" description="Recherche sur les sites de l'&#xC9;glise Catholique." language="fr"/> 
# </CustomSearchEngines>
class SearchEngineFromXml():
	def __init__(self, se_xml):
		self.title = se_xml.attributes['title'].value
		self.creator = se_xml.attributes['creator'].value
		self.cse_id = se_xml.attributes['id'].value
		self.cse_unique_id = "%s:%s" % (self.creator, self.cse_id)
		self.description = ""#se_xml.attributes['description'].value
		self.filter_label_name = "_cse_%s" % self.cse_id # C'est une convention ! Mais attention, rien n'empeche que ce soit different

# <?xml version="1.0" encoding="UTF-8" ?>
#   <Annotations start="0" num="2">
#     <Annotation about="*.cnn.com/*" score="1" timestamp="0x0004545f2e9f36cf" href="CgsqLmNubi5jb20vKhDP7fz08ouVAg">
#      <Label name="_cse_hg1shdcqrjs"/>
#      <AdditionalData attribute="original_url" value="cnn.com/*"/>
#     </Annotation>
#     <Annotation about="*.google.com/*" score="1" timestamp="0x0004585ba0c61ce4" href="Cg4qLmdvb2dsZS5jb20vKhDkuZiGuouWAg">
#      <Label name="_cse_qcfwlffvvrg"/>
#      <AdditionalData attribute="original_url" value="google.com/*"/>
#     </Annotation>
#   </Annotations> 
class AnnotationFromXml():
	def __init__(self, annotation_xml):
		self.about = annotation_xml.attributes['about'].value
		# self.score = annotation_xml.attributes['score'].value
		self.href = annotation_xml.attributes['href'].value
		
		self.label = annotation_xml.getElementsByTagName("Label")[0].attributes['name'].value
