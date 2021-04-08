$(document).ready(function () {

	$('.donateButton').on('click', function () {
		var gradId = $(this).attr('data-gradid');
		window.location.href = "/profile/" + gradId;
	});

	$('.searchForm').on('submit', function(e) {
		e.preventDefault();
		var q = $('.searchValue').val();
		window.location.href = "/makedonation?q=" + q;
	})


});