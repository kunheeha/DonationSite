$(document).ready(function () {

	$('.donateButton').on('click', function () {
		var gradId = $(this).attr('data-gradid');
		window.location.href = "/profile/" + gradId;
		
		// $.ajax({
		// 	type : 'POST',
		// 	url : '/',
		// 	data : {gradId:gradId},
		// 	success : function () {
		// 		console.log('works');
		// 		window.location.href = "/profile/" + gradId;
		// 	},
		// 	error : function() {
		// 		console.log("didnt work " + gradId);
		// 	}
		// });
	});


});