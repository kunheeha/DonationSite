$(document).ready(function () {

	$('.donateButton').on('click', function () {
		var gradId = $(this).attr('data-gradid');
		
		$.ajax({
			type : 'POST',
			url : '/',
			data : {gradId:gradId},
			success : function (data) {
				window.location.href = "/profile";
			},
			error : function() {
				console.log("didnt work " + gradId)
			}
		});
	});


});