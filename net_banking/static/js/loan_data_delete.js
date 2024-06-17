document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.delete-btn').forEach(function(button) {
        button.addEventListener('click', function(event) {
            const loanformDiv = this.closest('.loanform');
            if (!loanformDiv) {
                console.error('Parent loanform not found for delete button');
                return;
            }

            const loanId = loanformDiv.getAttribute('data-id');
            console.log('Deleting loan with ID:', loanId);

            // Send delete request to the server
            fetch(`/delete_loan/${loanId}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}', // Include CSRF token for security
                },
            })
            .then(response => {
                if (response.ok) {
                    // If deletion is successful, remove the card containing the loan
                    loanformDiv.closest('.card').remove();
                } else {
                    // If deletion fails, show an alert to the user
                    alert('Failed to delete loan');
                }
            })
            .catch(error => {
                // Log and alert if there's an error with the fetch request
                console.error('Error deleting loan:', error);
                alert('Failed to delete loan');
            });
        });
    });
});
