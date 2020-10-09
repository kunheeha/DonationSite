$(document).ready(function () {

	$("[data-fancybox]").fancybox({});

	$('#submitbutton').click(function(event) {
		event.preventDefault();
		$.post('/account', data=$('#aboutform').serialize(), function(data) {
			if (data.status == 'ok') {
				// $('#addDesc').hide();
				location.reload();
			} else {
				console.log('it didn\'t work')
			}
		});
	});







});