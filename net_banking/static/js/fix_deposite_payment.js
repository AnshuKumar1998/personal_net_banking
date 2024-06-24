function processPayment() {
    var isAuthenticated = JSON.parse(document.getElementById("is_authenticated").innerText);
    if (!isAuthenticated) {
        alert("You need to log in to make a payment.");
        return;
    }

    // Submit the form via AJAX
    var form = document.getElementById("paymentForm");
    var formData = new FormData(form);

    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Show success modal
            $('#successModal').modal('show');
        } else {
            alert("There was an error processing your payment. Please try again.");
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("There was an error processing your payment. Please try again.");
    });
}

function redirectToFixDepositList() {
    // Redirect to /activity/ page
    var activityPageUrl = "/activity/";
    window.location.href = activityPageUrl;
}
