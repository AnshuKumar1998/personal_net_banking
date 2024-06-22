// delete_account.js

document.getElementById('deleteAccountLink').addEventListener('click', function(event) {
    event.preventDefault();
    document.getElementById('deleteAccountModal').style.display = 'block';
});

document.getElementById('confirmDelete').addEventListener('click', function() {
    // Hide the modal
    closeModal();

    // Show progress overlay
    document.getElementById('progressOverlay').style.display = 'flex';

    // Make AJAX call to delete account
    fetch("{% url 'delete_account' %}", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}',
        },
        body: JSON.stringify({
            username: '{{ request.user.username }}'
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'error') {
            alert(data.message);
            document.getElementById('progressOverlay').style.display = 'none';
        } else {
            let progress = 0;
            const progressBar = document.getElementById('progressBar');
            const interval = setInterval(function() {
                if (progress >= 100) {
                    clearInterval(interval);
                    // Log out the user
                    fetch("{% url 'logout' %}", {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': '{{ csrf_token }}',
                        },
                    }).then(() => {
                        // Redirect to index page after completion
                        window.location.href = "{% url 'index' %}";
                    });
                } else {
                    progress += 10;
                    progressBar.style.width = progress + '%';
                    progressBar.innerText = 'Processing ' + progress + '%';
                }
            }, 500);
        }
    });
});

function closeModal() {
    document.getElementById('deleteAccountModal').style.display = 'none';
}
