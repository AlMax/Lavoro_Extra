$('#Pannello1 [data-toggle="tooltip"]').tooltip({
    animated: 'fade',
    placement: 'bottom',
    html: true,
	delay:500
});


var timeoutId;
$("area").hover(function() {
    if (!timeoutId) {
        timeoutId = window.setTimeout(function() {
            timeoutId = null; // EDIT: added this line
            $( "#Main_Page" ).fadeTo( "slow" , 0.1, function() {
				// Animation complete.
			});
       }, 500);
    }
},
function () {
    if (timeoutId) {
        window.clearTimeout(timeoutId);
        timeoutId = null;
    }
    else {
       $( "#Main_Page" ).fadeTo( "slow" , 1, function() {
			// Animation complete.
		});
    }
});