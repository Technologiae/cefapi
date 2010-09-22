(function($){

/**
 * Simple watermark plugin
 * 
 * @param defaultVal default null
 * @param color default #cccccc
 * @param fontStyle defualt italic
 * @return jQuery object
 */	
$.fn.extend({
    'fieldWaterMark' :function(options){
        var defaults = {
            'defaultVal'    : null,
            'color'         : '#cccccc'
        };
        
        options = $.extend(defaults, options);
        
        return this.each(function(){
            var $this = $(this);
            var currentVal = $.trim($this.val());
            
            $this.css({
                'color'         : options.color
            });
            
            if(currentVal.length <= 0 && options.defaultVal != null)
            {
                $this.val(options.defaultVal);
                currentVal = options.defaultVal;
            }
            
            $this.focus(function(){
                if($.trim($(this).val()) == currentVal)
                {
                    $(this).val('')
                    .css({
                        'color'         : '',
                        'font-style'    : ''
                    });
                }
            })
            .blur(function(){
                if($.trim($(this).val()).length <= 0)
                {
                    $(this).css({
                        'color'         : options.color,
                        'font-style'    : options.fontStyle
                    })
                    .val(currentVal);
                }
            });
        });
    }
});

// Menu plugin
// © PM Leveque
jQuery.fn.extend({ 
	cef_nav_menu: function() {
		var menus = $(this);
		
		var closetimer	= null;
		var active_menu = null;
		var timeout    	= 200;
		
		var close_all_menus = function() {
			active_menu = null;
			menus.each(function(){$(this).fadeOut(50);});
		};
		
		var start_timer = function() {
			if (active_menu) {
				closetimer = window.setTimeout(close_all_menus, timeout);
			}
		};
		
		var cancel_timer = function() {
			if (closetimer) {
				window.clearTimeout(closetimer);
				closetimer = null;
			}
		};
				
		//Iterate over the current set of matched elements
		return this.each(function(){
			var menu = $(this);
			var menu_title = menu.prev("a");
			
			var menu_show = function(){
				cancel_timer();
				if (active_menu != menu) {
					close_all_menus();
				}
				active_menu = menu;
				menu.css('left', menu_title.offset().left - 6);
				menu.show();
			};
			
			menu_title.click(function(){
				if (active_menu) {
					close_all_menus();
					}else{
					menu_show();
				}
				return false;
			});
			menu_title.mouseover(function(){
				if (active_menu) {menu_show()};
			});
			menu.mouseout(start_timer);
			menu.mouseover(cancel_timer);			
			
		});
	}
});


// CEF navigation bar
// © Pierre-Marie Lévêque
// L'affichage des résultats doit respecter les règles de Google:
// Guidelines for implementing Google™ Custom Search
// http://www.google.com/cse/docs/branding.html

var api_host = "{{host}}";
window.CEF = {};

CEF.settings = {
	site_search: {% ifequal navbar.cse_unique_id "recherche.catholique.fr" %}false{% else %}true{% endifequal %},
	share_links: true,
	google_search_restriction: {% if not navbar.cse_unique_id %}location.host{% else %}"{{ navbar.cse_unique_id }}"{% endif %},
	scrolling_bar: true,
	image_search_results: true,
	news_search_results: true
}

CEF.settings.google_search_restriction_label = "Pages de " + CEF.settings.google_search_restriction;

CEF.navigationBarHtml = "{{navbar_template}}";
CEF.searchResultsHtmlTemplate = "{{search_results_template}}";

// Function utilitaire
CEF.import_style = function (src){
	jQuery('head').append('<link rel="stylesheet" href="http://' + api_host + '/stylesheets/' + src + '" type="text/css" media="all" />');
}

// Triggers search event
CEF.search = function(query) {
	var remove_cef_search_floatbox = function(){
		$("div#cef_search_floatbox").remove();
		$("div#cef_search_floatbox_bg").remove();
		return false;
	}
	
	window.scrollTo(0,0);
	
	if (query == "" || query == "indiquez ici votre recherche...") {
		alert("Entrez le texte de votre recherche dans le rectangle à côté de la loupe !");
	}else{
		// Si la fenêtre est déjà affichée, on la supprime
		if ($("div#cef_search_floatbox").length) {
			remove_cef_search_floatbox();
		}

		$("body").append(CEF.searchResultsHtmlTemplate.replace(/%escaped_query%/g, encodeURI(query)).replace(/%query%/g, query));
		$("div#cef_search_floatbox").hide();
		$("div#cef_search_floatbox_bg").click(remove_cef_search_floatbox);
		$(".remove_cef_search_floatbox").click(remove_cef_search_floatbox);

		// Problèmes avec IE
		if ($.browser.msie) {
			$("#cef_search_floatbox_bg").css("background-color", "transparent");
		}

		// ===========================================
		// = Premier affichage: résultats de ce site =
		// ===========================================
		var thisSiteSearchControl = new google.search.SearchControl();
		thisSiteSearchControl.setResultSetSize(google.search.Search.SMALL_RESULTSET);
		// Set a callback so that whenever a search is started we will call XXX
		// thisSiteSearchControl.setSearchStartingCallback(this, XXX);

		thisSiteSearchControl.setSearchCompleteCallback(this, function(sc, searcher){
	         $("div#cef_search_floatbox").fadeIn("fast");
			if(webSearch.results.length==0){
				$("#this_site_search_results").html("Aucun résultat n'a été trouvé !");
			}
	    });

		// Web Search
		var webSearch = new google.search.WebSearch();
		webSearch.setUserDefinedLabel(CEF.settings.google_search_restriction_label);
		//FIXME
		webSearch.setSiteRestriction(CEF.settings.google_search_restriction);

		// News search
		var newsSearch = new google.search.NewsSearch();
		newsSearch.setSiteRestriction("Église");

		// Image Search
		var imageSearch = new google.search.ImageSearch();
		imageSearch.setUserDefinedLabel("Images");
		imageSearch.setSiteRestriction(CEF.settings.google_search_restriction);

		// Create 3 searchers and add them to the control
		thisSiteSearchControl.addSearcher(webSearch);
		if (CEF.settings.image_search_results) {
			thisSiteSearchControl.addSearcher(imageSearch);
		}
		if (CEF.settings.news_search_results) {
			thisSiteSearchControl.addSearcher(newsSearch);
		}

		// Set the options to draw the control in tabbed mode
		var drawOptions = new google.search.DrawOptions();
		drawOptions.setDrawMode(google.search.SearchControl.DRAW_MODE_TABBED);
		// drawOptions.setInput("site_search");

		thisSiteSearchControl.draw('this_site_search_results', drawOptions);

		thisSiteSearchControl.execute(query);
				
		// Google Analytics tracking
		if(typeof(pageTracker)!='undefined'){
			pageTracker._trackPageview('/?search_query=' + query);
		}
	}
	
}

// Fonction d'initialisation de la recherche
CEF.initializeSearch = function(){
	try {			
		$("#cef_search").submit(function(){
			var query = $("#site_search").attr("value");
			CEF.search(query);
			return false;
		});
		
	}catch(err){}
};
	
CEF.initNavigationBar = function(options){
	// Les options par défaut sont configurées dans la variable CEF.settings
	if (typeof(options) != 'undefined'){
		$.extend(CEF.settings, options);
	}

	// On désactive la recherche intégrée si l'API google n'a pas été initialisée
	if (typeof(google) == 'undefined'){
		$.extend(CEF.settings, {site_search: false});
	}

	// On ajoute le code HTML de la barre de navigation à l'élément #cef-root (ou sinon à <body>)
	if ($("#cef-root").length) {
		$("#cef-root").append(CEF.navigationBarHtml);
	}else{
		$("body").append(CEF.navigationBarHtml);
	}
	
	// On importe la feuille de style
	// La barre de navigation ne s'affiche qu'une fois cette feuille de style chargée.
	CEF.import_style("navigation_bar.1-0-2.css");
	
	// On active le fonctionnement des menus
	$("div.cef_nav_menu").cef_nav_menu();
	
	// On supprime les liens de partage si nécessaire
	if (!CEF.settings.share_links) {
		$("#cef_navigation_links_right").remove();
	}
	
	// La barre de navigation est "fixée" si demandé
	if (CEF.settings.scrolling_bar) {
		$("#cef_navigation").css({position: "fixed"});
	}
	
	// On active la recherche interne si demandé	
	if (CEF.settings.site_search) {
		CEF.import_style("site_search.1-0-2.css");
		google.load('search', '1', {language: 'fr', callback:CEF.initializeSearch, nocss:true });
		$('#site_search').fieldWaterMark({defaultVal: 'indiquez ici votre recherche...'});
	}else{
		$('#site_search').fieldWaterMark({defaultVal: 'recherche sites catholiques'});
	}
	
}

$(window).load(function(){
	$('#search_input_id').submit(function(){
		$("#site_search").attr("value", "");
		return false;
	})
});

if (window.cefAsyncInit) {
	cefAsyncInit();
}else{
	// Si la fonction d'initialisation asynchrone n'existe pas, on charge le script une fois la page "ready":
	$(function(){
		CEF.initNavigationBar();
	});
};
	
})(jQuery);
