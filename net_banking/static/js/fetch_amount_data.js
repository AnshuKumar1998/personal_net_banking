document.addEventListener('DOMContentLoaded', function () {
    var plusButton = document.getElementById('plusButton');
    var refreshButton = document.getElementById('refreshButton');
    var currentAmount = document.getElementById('currentAmount');
    var amountModal = new bootstrap.Modal(document.getElementById('amountModal'));
    var addAmountForm = document.getElementById('addAmountForm');

    // Handle plus button click to show modal
    plusButton.addEventListener('click', function () {
        amountModal.show();
    });

    // Handle form submission for adding amount
    addAmountForm.addEventListener('submit', function (event) {
        event.preventDefault();

        var amount = document.getElementById('amount').value;

        fetch('/update_amount/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Function to get CSRF token from cookies
            },
            body: JSON.stringify({ amount: amount })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                currentAmount.textContent = data.new_amount;
                amountModal.hide();
            } else {
                alert('Error updating amount.');
            }
        })
        .catch(error => console.error('Error:', error));
    });

    // Handle refresh button click to update current amount
    refreshButton.addEventListener('click', function () {
        fetch('/get_current_amount/')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                currentAmount.textContent = data.current_amount;
            } else {
                alert('Error fetching current amount.');
            }
        })
        .catch(error => console.error('Error:', error));
    });

    // Function to get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
