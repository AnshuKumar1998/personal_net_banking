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
            if (data.message === 'Money transferred successfully.') {
                showModal('Transfer Result', `<p>${data.message}</p>`);
                document.getElementById('currentAmount').textContent = data.current_amount;
            } else {
                showModal('Transfer Result', `<p>${data.message}</p>`);
            }
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