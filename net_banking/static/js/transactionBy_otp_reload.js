document.addEventListener('DOMContentLoaded', function() {

    var activateConfirmBtn = document.getElementById('activateConfirmBtn');


    addCustomerConfirmBtn.addEventListener('click', function() {
        // Perform AJAX request to add customer account
        fetch('/add_customer/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Fetch the CSRF token for security
            },
            body: JSON.stringify({
                transaction_account: document.getElementById('transactionAmount').innerText,
                transaction_pin: document.getElementById('transactionPin').innerText,
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload(); // Reload the page to see the new customer account
            } else {
                alert('Failed to add customer.');
            }
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

});
