document.addEventListener('DOMContentLoaded', function() {

    // Function to show Bootstrap modal with messages
    function showModal(title, message) {
        var modalEl = document.getElementById('messageModal');
        if (!modalEl) return;
        $('#messageModal .modal-title').text(title);
        $('#messageModal .modal-body').html(message);
        $('#messageModal').modal('show');
    }

    const searchButton = document.getElementById('searchButton');
    const transferButton = document.getElementById('transferButton');
    const transferForm = document.getElementById('transferForm');

    // Search button logic
    if (searchButton) {
        searchButton.addEventListener('click', function() {
            const accountInputEl = document.getElementById('accountInput');
            const errorEl = document.getElementById('accountInput_error');
            if (!accountInputEl || !errorEl) return;
            const accountInput = accountInputEl.value.trim();
            dvloader('show');

            if (!accountInput) {
                accountInputEl.classList.add("is-invalid");
                errorEl.style.display = "block";
                errorEl.style.color = "red";
               // errorEl.textContent = "Please enter an account number or UPI ID";
                dvloader('hide');
                return;
            }

            fetch(`/fetch-user-data/?accountInput=${encodeURIComponent(accountInput)}`)
            .then(response => response.json())
            .then(data => {
                const userDataEl = document.getElementById('userData');
                if (data.success) {
                    document.getElementById('userName').value = data.data.name;
                    document.getElementById('userEmail').value = data.data.email;
                    document.getElementById('userMobile').value = data.data.mobile;
                    if (userDataEl) userDataEl.style.display = 'block';
                } else {
                    alert('User not found');
                    document.getElementById('userName').value = '';
                    document.getElementById('userEmail').value = '';
                    document.getElementById('userMobile').value = '';
                    if (userDataEl) userDataEl.style.display = 'none';
                }
                setTimeout(() => dvloader('hide'), 400);
            })
            .catch(error => {
                console.error('An error occurred:', error);
                showModal('Error', '<p>An error occurred while fetching user data.</p>');
                document.getElementById('userName').value = '';
                document.getElementById('userEmail').value = '';
                document.getElementById('userMobile').value = '';
                const userDataEl = document.getElementById('userData');
                if (userDataEl) userDataEl.style.display = 'none';
                setTimeout(() => dvloader('hide'), 400);
            });
        });
    }

    const accountInputEl = document.getElementById('accountInput');
    const errorEl = document.getElementById('accountInput_error');

    if (accountInputEl && errorEl) {
        accountInputEl.addEventListener('focus', function () {
            accountInputEl.classList.remove("is-invalid");
            errorEl.style.display = "none";
            errorEl.textContent = "";
        });
    }

    // Transfer button logic
    if (transferButton) {
    transferButton.addEventListener('click', function() {
        dvloader('show');
        const accountInputEl = document.getElementById('accountInput');
        const amountEl = document.getElementById('transferAmount');
        const errorEl = document.getElementById('transferAmount_error');

        if (!amountEl.value.trim()) {
            amountEl.classList.add("is-invalid");
            errorEl.style.display = "block";
            errorEl.style.color = "red";
            //errorEl.textContent = "Please enter amount";
            dvloader('hide');
            return;
        }

        if (!accountInputEl.value.trim()) {
            accountInputEl.classList.add("is-invalid");
            // similarly show error for account input if needed
            dvloader('hide');
            return;
        }

        const account = accountInputEl.value.trim();
        const amount = parseFloat(amountEl.value.trim()) || 0;

        fetch('/transfer_money/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: JSON.stringify({ account, amount })
        })
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            showModal('Transfer Result', `<p>${data.message}</p>`);
        })
        .catch(error => {
            console.error('Error during fetch operation:', error);
            showModal('Error', '<p>An error occurred while processing your request.</p>');
        })
        .finally(() => {
            setTimeout(() => dvloader('hide'), 400);
        });
    });
}
const amountEl2 = document.getElementById('transferAmount');
const errorEl2 = document.getElementById('transferAmount_error');
     if (amountEl2 && errorEl2) {
        amountEl2.addEventListener('focus', function () {
            amountEl2.classList.remove("is-invalid");
            errorEl2.style.display = "none";
            errorEl2.textContent = "";
        });
    }

    // Prevent default form submission for transferForm
    if (transferForm) {
        transferForm.addEventListener('submit', function(e) {
            e.preventDefault();
            // Optional: you can call transferButton.click() here to trigger AJAX
        });
    }

});
