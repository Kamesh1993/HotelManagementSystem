(function($) {
	
	"use strict";
	
	// Cache Selectors
	var mainDocument	=$(document),
		video			=$('.popup-youtube');


	//Magnific Video 
	mainDocument.on('ready', function() {
		video.magnificPopup({
		  disableOn: 700,
		  type: 'iframe',
		  mainClass: 'mfp-fade',
		  removalDelay: 160,
		  preloader: false,
		  fixedContentPos: false
		});
	});

})(jQuery);