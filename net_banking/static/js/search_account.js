document.addEventListener('DOMContentLoaded', function() {
    // Function to show Bootstrap modal with messages
    function showModal(title, message) {
        $('#messageModal .modal-title').text(title);
        $('#messageModal .modal-body').html(message);
        $('#messageModal').modal('show');
    }

    // Event listener for Search button
    document.getElementById('searchButton').addEventListener('click', function() {
        var accountInput = document.getElementById('accountInput').value;
        console.log('Search button clicked. Account input:', accountInput); // Debugging line
        if (accountInput) {
            // Fetch user data based on account number or UPI ID
            fetch(`/fetch-user-data/?accountInput=${encodeURIComponent(accountInput)}`)
                .then(response => response.json())
                .then(data => {
                    console.log('Server response:', data); // Debugging line
                    if (data.success) {
                        document.getElementById('userName').value = data.data.name;
                        document.getElementById('userEmail').value = data.data.email;
                        document.getElementById('userMobile').value = data.data.mobile;
                        document.getElementById('userData').style.display = 'block';
                    } else {
                        alert('User not found');
                        document.getElementById('userName').value = '';
                        document.getElementById('userEmail').value = '';
                        document.getElementById('userMobile').value = '';
                        document.getElementById('userData').style.display = 'none';
                    }
                })
                .catch(error => {
                    console.error('An error occurred:', error); // Debugging line
                    alert('An error occurred while fetching user data.');
                    document.getElementById('userName').value = '';
                    document.getElementById('userEmail').value = '';
                    document.getElementById('userMobile').value = '';
                    document.getElementById('userData').style.display = 'none';
                });
        } else {
            alert('Please enter an account number or UPI ID');
        }
    });

    // Event listener for Transfer Now button
    document.getElementById('transferButton').addEventListener('click', function() {
        var account = document.getElementById('accountInput').value;
        var amount = parseFloat(document.getElementById('transferAmount').value);

        // Perform AJAX request to transfer money
        fetch('/transfer_money/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: JSON.stringify({
                account: account,
                amount: amount
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Handle server response
            showModal('Transfer Result', `<p>${data.message}</p>`);
        })
        .catch(error => {
            console.error('Error during fetch operation:', error);
            showModal('Error', '<p>An error occurred while processing your request.</p>');
        });
    });

    // Prevent default form submission for transferForm
    document.getElementById('transferForm').addEventListener('submit', function(e) {
        e.preventDefault();
        // Add your form submission logic here if needed
    });
});

