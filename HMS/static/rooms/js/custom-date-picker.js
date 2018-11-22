(function($) {
	
	"use strict";

	// Cache Selectors
	var date1			=$('.dpd1'),
		date2			=$('.dpd2');
	
	
	//Date Picker//
	var nowTemp = new Date();
	var now = new Date(nowTemp.getFullYear(), nowTemp.getMonth(), nowTemp.getDate(), 0, 0, 0, 0);
	 
	var checkin = date1.datepicker({
		onRender: function(date) {
			return date.valueOf() < now.valueOf() ? 'disabled' : '';
		}
	}).on('changeDate', function(ev) {
		if (ev.date.valueOf() > checkout.date.valueOf()) {
			var newDate = new Date(ev.date)
			newDate.setDate(newDate.getDate() + 1);
			checkout.setValue(newDate);
		}
		
		checkin.hide();
		date2[0].focus();
		
	}).data('datepicker');
	
	var checkout = date2.datepicker({
		onRender: function(date) {
			return date.valueOf() <= checkin.date.valueOf() ? 'disabled' : '';
		}
		
	}).on('changeDate', function(ev) {
		checkout.hide();
	}).data('datepicker');
	

})(jQuery);