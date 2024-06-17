document.addEventListener('DOMContentLoaded', function() {
    // Attach click event to each message for viewing details
    document.querySelectorAll('.message').forEach(function(message) {
        message.addEventListener('click', function(event) {
            if (event.target.classList.contains('delete-btn')) {
                return; // Ignore the click if it's on the delete button
            }
            const subject = this.getAttribute('data-subject');
            const content = this.getAttribute('data-content');
            const date = this.getAttribute('data-date');

            // Populate modal with message details
            document.getElementById('modalSubject').innerText = subject;
            document.getElementById('modalContent').innerText = content;
            document.getElementById('modalDate').innerText = date;

            // Show the modal
            $('#messageModal').modal('show');
        });
    });

    // Attach click event to each delete button
    document.querySelectorAll('.delete-btn').forEach(function(button) {
        button.addEventListener('click', function(event) {
            const messageDiv = this.closest('.message');
            const messageId = messageDiv.getAttribute('data-id');

            // Send delete request to the server
            fetch(`/delete_message/${messageId}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}', // Include CSRF token for security
                },
            })
            .then(response => {
                if (response.ok) {
                    messageDiv.remove(); // Remove message div from the DOM
                } else {
                    alert('Failed to delete message');
                }
            })
            .catch(error => {
                console.error('Error deleting message:', error);
                alert('Failed to delete message');
            });
        });
    });
});
