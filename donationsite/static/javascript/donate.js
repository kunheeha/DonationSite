function runStripe() {
	var stripe = Stripe('pk_test_51HjmAVHu9SvbXNkQAypv6sJP5a3ySE9slgtPbzvOyeHoGzP5ytQMnqqDKiVH25GjgfdzwovilTmi1reAZkt8KiMN00lJID3ZHk');


	fetch('/create-checkout-session', {
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
		$.ajax({
			type : 'POST',
			url : '/success',
			data : {gradname:gradName},
			success : function (data) {
				console.log('Success' + data);
			},
			error : function() {
				console.log("didnt work " + gradName)
			}
		});
		runStripe();
	});

})




// var stripe = Stripe('pk_test_51HjmAVHu9SvbXNkQAypv6sJP5a3ySE9slgtPbzvOyeHoGzP5ytQMnqqDKiVH25GjgfdzwovilTmi1reAZkt8KiMN00lJID3ZHk');
// var checkoutButton = document.getElementById('checkout-button');
// var gradName = checkoutButton.dataset.gradname;
// var testButton = document.getElementById('testbutton')


// checkoutButton.addEventListener('click', function() {
// 	fetch('/create-checkout-session', {
// 		method: 'POST'
// 	})
// 	.then(function(response) {
// 		return response.json();
// 	})
// 	.then(function(session) {
// 		return stripe.redirectToCheckout({ sessionId: session.id });
// 	})
// 	.then(function(result) {
// 		if (result.error) {
// 			alert(result.error.message);
// 		}
// 	})
// 	.catch(function(error) {
// 		console.error('Error: ', error);
// 	});

// });

