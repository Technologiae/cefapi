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


// Functions utilitaires
var import_script = function (src){
	jQuery('head').append('<script src="' + src + '" type="text/javascript"></script>');
}

var import_style = function (src){
	jQuery('head').append('<link rel="stylesheet" href="http://' + api_host + '/stylesheets/' + src + '" type="text/css" media="all" />');
}


// CEF navigation bar
// © Pierre-Marie Lévêque
// L'affichage des résultats doit respecter les règles de Google:
// Guidelines for implementing Google™ Custom Search
// http://www.google.com/cse/docs/branding.html

var api_host = "{{host}}";

var settings = {
	site_search: true,
	share_links: true,
	add_top_margin: false,
	with_animation: true,
	google_search_restriction: location.host,
	cef_root: "#cef-root",
	scrolling_bar: true
}

// Si l'élément <div id="cef-root"></div> n'existe pas
if (!$(settings.cef_root).length) {
	settings.cef_root = "body";
}

// Ajouter les options dans la variable "cef_nav_options", à ajouter dans le code avant ce script.
if (typeof(cef_nav_options) != 'undefined'){
	$.extend(settings, cef_nav_options);
}

// On désactive la recherche intégrée si l'API google n'a pas été initialisée
if (typeof(google) == 'undefined'){
	$.extend(settings, {site_search: false});
}

// Fonction d'initialisation de la recherche
var initializeSearch = function(){
	try {			
		$("#cef_search").submit(function(){
			var query = $("#site_search").attr("value");

			var remove_cef_search_floatbox = function(){
				$("div#cef_search_floatbox").remove();
				$("div#cef_search_floatbox_bg").remove();
				return false;
			}
			
			window.scrollTo(0,0);
			
			$("body").append("<div id='cef_search_floatbox'><img id='google_custom_search_logo_img' src='http://www.google.com/cse/images/google_custom_search_smnar.gif' /><h2 id='cef_search_results_h2'>R&eacute;sultats pour \""+ query +"\"</h2><span class='remove_cef_search_floatbox' id='cef_close_floatbox'>X</span><div id='this_site_search_results'></div><div class='clear'></div><p id='search_explanation'><a href=\"http://recherche.catholique.fr/?q="+ query +"\">Rechercher \""+ query +"\" sur recherche.catholique.fr</a><br /><br />Découvrez le site <a href=\"http://recherche.catholique.fr/?q="+ query +"\">recherche.catholique.fr</a>, pour rechercher sur tous les sites des <strong>dioc&egrave;ses</strong>, des <strong>services nationaux</strong> de la CEF, et sur les sites en <strong>.cef.fr</strong> et en <strong>.catholique.fr</strong></p><p><a href='#' class='remove_cef_search_floatbox'>Fermer cette fen&ecirc;tre</a></p></div>")
			$("body").append("<div id='cef_search_floatbox_bg'></div>");
			$("div#cef_search_floatbox_bg").css({position:"fixed",zIndex:999999998,width:"100%",height:"100%",top:"0px",left:"0px",backgroundColor:"#000",opacity:"0.20"});
			$("div#cef_search_floatbox_bg").click(remove_cef_search_floatbox);
			$(".remove_cef_search_floatbox").click(remove_cef_search_floatbox);
			
			// ===========================================
			// = Premier affichage: résultats de ce site =
			// ===========================================
			var thisSiteSearchControl = new google.search.SearchControl();
			thisSiteSearchControl.setResultSetSize(google.search.Search.LARGE_RESULTSET);
			// Set a callback so that whenever a search is started we will call XXX
			// thisSiteSearchControl.setSearchStartingCallback(this, XXX);

			// Web Search
			var webSearch = new google.search.WebSearch();
			webSearch.setUserDefinedLabel("Pages de " + settings.google_search_restriction);
			//FIXME
			webSearch.setSiteRestriction(settings.google_search_restriction);

			// News search
			var newsSearch = new google.search.NewsSearch();
			newsSearch.setSiteRestriction("Église");

			// Image Search
			var imageSearch = new google.search.ImageSearch();
			imageSearch.setUserDefinedLabel("Images");
			imageSearch.setSiteRestriction(settings.google_search_restriction);

			// Create 3 searchers and add them to the control
			thisSiteSearchControl.addSearcher(webSearch);
			thisSiteSearchControl.addSearcher(imageSearch);
			thisSiteSearchControl.addSearcher(newsSearch);

			// Set the options to draw the control in tabbed mode
			var drawOptions = new google.search.DrawOptions();
			drawOptions.setDrawMode(google.search.SearchControl.DRAW_MODE_TABBED);
			// drawOptions.setInput("site_search");

			thisSiteSearchControl.draw('this_site_search_results', drawOptions);
			
			if (query == "") {}else{
				thisSiteSearchControl.execute(query);
				// Google Analytics tracking
				if(typeof(pageTracker)!='undefined'){
					pageTracker._trackPageview('/search?kind=site_search&q=' + query);
				}
			}

			return false;
		});

	}catch(err){}
};
	
var initializeCefNav = function(){
	$(settings.cef_root).append("{{navigation_bar_template}}");
	
	import_style("navigation_bar.0-4.css");
	
	$("div.cef_nav_menu").cef_nav_menu();
		
	if (!settings.share_links) {
		$("#cef_navigation_links_right").remove();
	}
	
	if (settings.add_top_margin) {
		if (settings.with_animation) {
			$("#cef_navigation").css({top:-24}).animate({top:0}, 500);
			$("body").animate({"margin-top":24}, 500);
		}else{
			$("body").css({"margin-top":24});
		}
		
	}
	
	if (settings.scrolling_bar) {
		$("#cef_navigation").css({position: "fixed"});
	}
		
	if (settings.site_search) {
		import_style("site_search.0-4.css");
		google.load('search', '1', {language: 'fr', callback:initializeSearch, nocss:true });
		$('#site_search').fieldWaterMark({defaultVal: 'Recherche dans ce site...'});
	}else{
		$('#site_search').fieldWaterMark({defaultVal: 'recherche.catholique.fr'});
	}
	
}

if (settings.cef_root == "body") {
	// L'initialisation a lieu une fois la page HTML chargée:
	$(initializeCefNav);
}else{
	// L'initialisation a lieu immédiatement
	initializeCefNav();
}
	
})(jQuery);
