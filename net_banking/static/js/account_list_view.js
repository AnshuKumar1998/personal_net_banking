$(document).ready(function() {
    $('#listButton').click(function() {
        fetchCustomerAccounts();

    });

   function fetchCustomerAccounts() {
    dvloader('show');

    $.ajax({
        url: '/api/get_customer_accounts/',
        type: 'GET',
        success: function(data) {
            $('#customerListModal').remove();

            let popupContent = `
            <div id="customerListModal" class="modal" tabindex="-1" role="dialog">
                <div class="modal-dialog modal-lg" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Select Customer Account</h5>
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div class="modal-body" style="max-height: 400px; overflow-y: auto;">
            `;

            if (data.length > 0) {
                popupContent += `<table class="table">
                    <thead><tr><th>Select</th><th>Account No</th><th>Name</th><th>Email</th><th>Mobile</th></tr></thead>
                    <tbody>`;

                data.forEach(item => {
                    popupContent += `<tr>
                        <td><button type="button" class="btn btn-primary select-customer-btn"
                            data-account-no="${item.customer_account_no}"
                            data-name="${item.customer_name}"
                            data-email="${item.customer_email}"
                            data-mobile="${item.customer_mobile_no}">Select</button></td>
                        <td>${item.customer_account_no}</td>
                        <td>${item.customer_name}</td>
                        <td>${item.customer_email}</td>
                        <td>${item.customer_mobile_no}</td>
                    </tr>`;
                });

                popupContent += `</tbody></table>`;
            } else {
                 popupContent += `<div class="alert alert-info text-start mt-3">
                        <i class="fa fa-exclamation-circle"></i>
                        <span class="ms-2">No customer accounts found.</span>
                    </div>
                `;
            }

            popupContent += `
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                        </div>
                    </div>
                </div>
            </div>
            `;

            $('body').append(popupContent);
            $('#customerListModal').modal('show');

            // Select button event
            $('.select-customer-btn').click(function() {
                const selected = $(this);
                $('#userName').val(selected.data('name'));
                $('#userEmail').val(selected.data('email'));
                $('#userMobile').val(selected.data('mobile'));
                $('#accountInput').val(selected.data('account-no'));
                $('#userData').show();
                $('#customerListModal').modal('hide');
            });

            $('#customerListModal').on('hidden.bs.modal', function() {
                $(this).remove();
            });

            dvloader('hide');
        },
        error: function(xhr, status, error) {
            dvloader('hide');
            alert('Failed to fetch customer accounts: ' + error);
        }
    });
}

});
