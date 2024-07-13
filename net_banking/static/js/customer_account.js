document.addEventListener('DOMContentLoaded', function() {
    var addCustomerBtn = document.getElementById('addCustomerBtn');
    var addCustomerModal = document.getElementById('addCustomerModal');
    var verifyBtn = document.getElementById('verifyBtn');
    var accountDetails = document.getElementById('accountDetails');
    var addCustomerConfirmBtn = document.getElementById('addCustomerConfirmBtn');
    var verifyAccountForm = document.getElementById('verifyAccountForm');

    addCustomerBtn.addEventListener('click', function() {
        $(addCustomerModal).modal('show');
    });

    verifyBtn.addEventListener('click', function() {
        var accountNo = document.getElementById('account_no').value;

        // Perform AJAX request to verify account number
        fetch('/verify_account/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Fetch the CSRF token for security
            },
            body: JSON.stringify({ account_no: accountNo })
        })
        .then(response => response.json())
        .then(data => {
            if (data.exists) {
                document.getElementById('accountName').innerText = data.name;
                document.getElementById('accountNumber').innerText = data.account_no;
                document.getElementById('mobileNo').innerText = data.mobile_no;
                document.getElementById('emailId').innerText = data.email_id;
                accountDetails.style.display = 'block';
            } else {
                alert('Account number not found.');
            }
        });
    });

    addCustomerConfirmBtn.addEventListener('click', function() {
        // Perform AJAX request to add customer account
        fetch('/add_customer/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Fetch the CSRF token for security
            },
            body: JSON.stringify({
                account_no: document.getElementById('accountNumber').innerText,
                name: document.getElementById('accountName').innerText,
                mobile_no: document.getElementById('mobileNo').innerText,
                email_id: document.getElementById('emailId').innerText
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

    // Function to delete customer
    function deleteCustomer(accountNo) {
        if (confirm("Are you sure you want to delete?")) {
            fetch(`/delete_customer/${accountNo}/`, {
                method: "DELETE",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "Content-Type": "application/json"
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.querySelector(`tr[data-account-no='${accountNo}']`).remove();
                    } else {
                        alert("Error deleting account.");
                    }
                })
                .catch(error => console.error("Error:", error));
        }
    }

    // Add event listener to customerAccountList for delete buttons
    document.getElementById('customerAccountList').addEventListener('click', function(event) {
        if (event.target.classList.contains('delete-btn2')) {
            const accountNo = event.target.closest('tr').dataset.accountNo;
            deleteCustomer(accountNo);
        }
    });
});
