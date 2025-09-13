
$(document).ready(function() {
    // Handle form submission
    $('#addAmountForm').submit(function(e) {
        e.preventDefault();
        var amount = $('#amount').val();
        dvloader('show');

        // AJAX request to update amount
        $.ajax({
            type: 'POST',
            url: '/update_amount/',
            data: JSON.stringify({'amount': amount}),
            contentType: 'application/json',
            success: function(response) {
                if (response.success) {
                    // Update success message in modal
                    $('#successMessage2').text(response.message);

                    // Update current amount display
                    $('#currentAmount').text(response.new_amount);

                    // Show success modal
                    $('#successModal2').modal('show');
                    setTimeout(() => {
                        dvloader('hide');
                    }, 400);
                } else {
                    alert('Failed to add money.');
                    setTimeout(() => {
                        dvloader('hide');
                    }, 400);
                }
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                setTimeout(() => {
                    dvloader('hide');
                }, 400);
            }
        });
    });

    // Close modal and update current amount display
    $('#successModal2').on('hidden.bs.modal', function() {
        // Optionally refresh page or perform additional actions
    });
});
