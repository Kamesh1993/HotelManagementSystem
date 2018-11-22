$(document).ready(function(){
	
	
	// contact forms validation
	$('#frm_contact').validate({
		
	      errorPlacement: function(error, element) {
			 return true;
			 
		  }, 
		
		  rules: {
		   txt_name: {
			minlength: 2,
			required: true,
		   },
		   txt_email: {
			required: true,
			email: true,
		   },
		   txt_phone: {
			required: true,
		   },
		  txt_message: {
			minlength: 2,
			required: true,
		   },
		  
		  },
		  
		  submitHandler: function( form ) {
			   
				$.ajax({
					url :  'email/contact-email-process.php',
					data : $('#frm_contact').serialize(),
					type: "POST",
					success : function(data){
						
						if(data=="sent") {
							$('#result_msg').html("<div class='col-sm-12 text-center alert alert-success'>Thank you for contacting us. We will be in touch with you soon.</div>");
						} else {
						
							$('#result_msg').html("<div class='col-sm-12 text-center alert alert-danger'>We are sorry, but there appears to be a problem with the form you submitted.</div>");
						}
						
					}
				})
				return false;
			 }
		  
		 });  // end contact forms validation
		 
		 
		 // booking forms validation
	$('#frm_booking').validate({
		
	      errorPlacement: function(error, element) {
			 return true;
			 
		  }, 
		
		  rules: {
		   txt_first_name: {
			minlength: 2,
			required: true,
		   },
		   txt_email: {
			required: true,
			email: true,
		   },
		   txt_phone: {
			required: true,
		   },
		    txt_arrival_date: {
			required: true,
		   },
		    txt_departure_date: {
			required: true,
		   },
		    txt_adults: {
			required: true,
		   },
		  txt_message: {
			minlength: 2,
			required: true,
		   },
		  
		  },
		  
		  submitHandler: function( form ) {
			   
				$.ajax({
					url :  'email/booking-email-process.php',
					data : $('#frm_booking').serialize(),
					type: "POST",
					success : function(data){
						if(data=="sent") {
							$('#result_msg').html("<div class='col-sm-12 text-center alert alert-success'>Thank you for contacting us. We will be in touch with you soon.</div>");
						} else {
						
							$('#result_msg').html("<div class='col-sm-12 text-center alert alert-danger'>We are sorry, but there appears to be a problem with the form you submitted.</div>");
						}
						
					}
				})
				return false;
			 }
		  
		 });  


	}); 