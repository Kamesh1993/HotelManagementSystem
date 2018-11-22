(function($) {
	
	"use strict";
	
	// Cache Selectors
	var myGallery		=$('.image-link'),
		filterButton	=$('.filter-button'),
		filter			=$('.filter');
	
	
	// Gallery
	myGallery.magnificPopup({
		
		type: 'image',
		closeBtnInside: true,
		mainClass: 'mfp-with-zoom mfp-img-mobile',
	
		gallery: {
			enabled: true 
		}
	});
	
	
	// Filter Buttons
	var $btns = filterButton.on('click',function() {
		
		var value = $(this).attr('data-filter');
		
		if (value == 'filter') {
			filter.show('1000');
		} 
		
		else {
			filter.not('.'+value).hide('3000');
			filter.filter('.'+value).show('3000');
		}
		
		$btns.removeClass('active');
		$(this).addClass('active');
	});

})(jQuery);

