$(document).ready(function() {
    $('.chatbot').hide();
	$('.chatbutton').click(function(){
		var innerhtml = $('.chatbutton').html();
		if (innerhtml==="Show Chatbot"){
			$('.chatbutton').html("Hide Chatbot");
			$('.chatbot').show();
			}
		if (innerhtml==="Hide Chatbot"){
			$('.chatbutton').html("Show Chatbot");
			$('.chatbot').hide();
			}
		
		}
	);
});

