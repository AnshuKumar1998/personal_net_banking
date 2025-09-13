document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.delete-btn').forEach(function(button) {
        button.addEventListener('click', function(event) {
            const messageDiv = this.closest('.message');
            if (!messageDiv) {
                console.error('Parent message not found for delete button');
                return;
            }

            const messageId = messageDiv.getAttribute('data-id');
            console.log('Deleting message with ID:', messageId);

            fetch(`/delete_message/${messageId}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',
                },
            })
            .then(response => {
                if (response.ok) {
                    // remove the message
                    messageDiv.remove();

                    // check agar koi message nahi bacha
                    const container = document.querySelector('.scrollable');
                    if (container.querySelectorAll('.message').length === 0) {
                        container.innerHTML = `
                             <i class="fa fa-inbox" aria-hidden="true"></i> Inbox is Empty
                        `;
                    }
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
