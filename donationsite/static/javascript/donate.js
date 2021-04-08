function runStripe(gradName) {
	var stripe = Stripe('pk_test_51HjmAVHu9SvbXNkQAypv6sJP5a3ySE9slgtPbzvOyeHoGzP5ytQMnqqDKiVH25GjgfdzwovilTmi1reAZkt8KiMN00lJID3ZHk');


	fetch('/create-checkout-session/' + gradName, {
		method: 'POST'
	})
	.then(function(response) {
		return response.json();
	})
	.then(function(session) {
		return stripe.redirectToCheckout({ sessionId: session.id });
	})
	.then(function(result) {
		if (result.error) {
			alert(result.error.message);
		}
	})
	.catch(function(error) {
		console.error('Error: ', error);
	});
}

$(document).ready(function () {



	$('.donationButton').on('click', function() {
		var gradName = $(this).attr('data-gradname');
		runStripe(gradName);


	});

})



