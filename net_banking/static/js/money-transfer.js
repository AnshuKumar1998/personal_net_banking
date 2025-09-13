// Event listener for Transfer Now button
const transferBtn = document.getElementById('transferButton');
if (transferBtn) {
    transferBtn.addEventListener('click', function() {
        var account = document.getElementById('accountInput').value;
        var amount = parseFloat(document.getElementById('transferAmount').value);

        // Perform AJAX request to transfer money
        dvloader('show');
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
            if (data.current_amount) {
                document.getElementById('currentAmount').textContent = data.current_amount;
            }
            setTimeout(() => {
                dvloader('hide');
            }, 400);
        })
        .catch(error => {
            console.error('Error during fetch operation:', error);
            setTimeout(() => {
                dvloader('hide');
                showModal('Error', '<p>An error occurred while processing your request.</p>');
            }, 200);
        });
    });
}

// Prevent default form submission for transferForm
const transferFormConst = document.getElementById('transferForm');
if (transferFormConst) {
    transferFormConst.addEventListener('submit', function(e) {
        e.preventDefault();
        // Custom logic if needed
    });
}
