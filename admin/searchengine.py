from admin_classes import *

# # XML parser: http://code.google.com/p/python-elements/
# from elements import Element
# 
# class CustomSearchEngine(Element):
# 	_tag = 'CustomSearchEngine'
# 	_attributes = Element._attributes.copy()
# 	_attributes['identifier'] = 'id'
# 	_attributes['creator'] = 'creator'
# 	_attributes['language'] = 'language'
# 	_children = Element.copy_children()	
# 	_children['Title'] = ('title', unicode)
# 	_children['Description'] = ('description', unicode)
# 
# 	def __init__(self, identifier=None, creator=None, language=None, title=None, description=None):
# 		self.identifier = identifier
# 		self.creator = creator
# 		self.language = language
# 		self.title = title
# 		self.description = description
# 
# class CustomSearchEngines(Element):
# 	_tag = 'CustomSearchEngines'
# 	_children = Element.copy_children()	
# 	_children['CustomSearchEngine'] = ('customsearchengines', [CustomSearchEngine])
# 	
# 	def __init__(self, customsearchengines=None):
# 		self.customsearchengines = customsearchengines or []
# 

# class Label(Element):
#	 _tag = 'Label'
#	 _attributes = Element._attributes.copy()
#	 _attributes['name'] = 'name'
#	 
#	 def __init__(self, name=None):
#		 self.name = name
# 
# class Annotation(Element):
#	 _tag = 'Annotation'
#	 _attributes = Element._attributes.copy()
#	 _attributes['about'] = 'about'
#	 _children = Element.copy_children()	
#	 _children['Label'] = ('label', Label)
# 
#	 def __init__(self, about=None, label=None):
#		 self.label = label
#		 self.about = about


class SearchenginePage(webapp.RequestHandler):
	def get(self, cse_id):
		gdatafeed = GdataFeed("http://www.google.com/cse/api/default/cse/%s" % cse_id)
		# searchengine = SearchEngine(gdatafeed.root_element())
		
		path = os.path.join(os.path.dirname(__file__), 'templates/searchengine.html')
		self.response.out.write(template.render(path, {'response': unicode(gdatafeed.response, errors="ignore"), 'searchengine': ""}))

class SearchenginesPage(webapp.RequestHandler):
	def get(self):		
		gdatafeed = GdataFeed("http://www.google.com/cse/api/default/cse/")
		searchengines = map(lambda cse_xml: SearchEngineFromXml(cse_xml), gdatafeed.elements("CustomSearchEngine"))
		
		gdatafeed2 = GdataFeed("http://www.google.com/cse/api/default/annotations/?num=5000")
		annotations =  map(lambda annotation_xml: AnnotationFromXml(annotation_xml), gdatafeed2.elements("Annotation"))

		path = os.path.join(os.path.dirname(__file__), 'templates/searchengines.html')
		self.response.out.write(template.render(path, {
														'response': unicode(gdatafeed2.response, errors="ignore"),
														'searchengines': searchengines,
														'annotations': annotations
														}))
		