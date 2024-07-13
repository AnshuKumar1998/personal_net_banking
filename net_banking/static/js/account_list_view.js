$(document).ready(function() {
    $('#listButton').click(function() {
        fetchCustomerAccounts();
    });

    function fetchCustomerAccounts() {
        $.ajax({
            url: '/api/get_customer_accounts/',  // Adjust the URL as per your setup
            type: 'GET',
            success: function(data) {
                // Remove existing modal if it exists
                $('#customerListModal').remove();

                var popupContent = '<div id="customerListModal" class="modal" tabindex="-1" role="dialog">';
                popupContent += '<div class="modal-dialog modal-lg" role="document">';
                popupContent += '<div class="modal-content">';
                popupContent += '<div class="modal-header">';
                popupContent += '<h5 class="modal-title">Select Customer Account</h5>';
                popupContent += '<button type="button" class="close" data-dismiss="modal" aria-label="Close">';
                popupContent += '<span aria-hidden="true">&times;</span></button></div>';

                // Set max height and enable scrolling
                popupContent += '<div class="modal-body" style="max-height: 400px; overflow-y: auto;">';
                popupContent += '<table class="table">';
                popupContent += '<thead><tr><th>Select</th><th>Account No</th><th>Name</th><th>Email</th><th>Mobile</th></tr></thead>';
                popupContent += '<tbody>';

                for (var i = 0; i < data.length; i++) {
                    popupContent += '<tr>';
                    popupContent += '<td><button type="button" class="btn btn-primary select-customer-btn" data-account-no="' + data[i].customer_account_no + '" data-name="' + data[i].customer_name + '" data-email="' + data[i].customer_email + '" data-mobile="' + data[i].customer_mobile_no + '">Select</button></td>';
                    popupContent += '<td>' + data[i].customer_account_no + '</td>';
                    popupContent += '<td>' + data[i].customer_name + '</td>';
                    popupContent += '<td>' + data[i].customer_email + '</td>';
                    popupContent += '<td>' + data[i].customer_mobile_no + '</td>';
                    popupContent += '</tr>';
                }

                popupContent += '</tbody></table>';
                popupContent += '</div>'; // modal-body
                popupContent += '<div class="modal-footer">';
                popupContent += '<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>';
                popupContent += '</div>'; // modal-footer
                popupContent += '</div>'; // modal-content
                popupContent += '</div>'; // modal-dialog
                popupContent += '</div>'; // customerListModal

                $('body').append(popupContent);
                $('#customerListModal').modal('show');

                // Add event listener to select buttons
                $('.select-customer-btn').click(function() {
                    var selectedCustomer = $(this);
                    $('#userName').val(selectedCustomer.data('name'));
                    $('#userEmail').val(selectedCustomer.data('email'));
                    $('#userMobile').val(selectedCustomer.data('mobile'));
                    $('#accountInput').val(selectedCustomer.data('account-no'));

                    $('#userData').show();
                    $('#customerListModal').modal('hide');
                });
            },
            error: function() {
                alert('Failed to fetch customer accounts.');
            }
        });
    }
});
