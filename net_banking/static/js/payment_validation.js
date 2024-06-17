  document.addEventListener('DOMContentLoaded', function () {
    var toastEl = document.getElementById('toastMessage');
    var paymentForm = document.getElementById('paymentForm');
    var total = {{ total }};

    paymentForm.addEventListener('submit', function(event) {
        var payAmt = parseFloat(document.getElementById('pay_amt').value);

        if (payAmt > total) {
            event.preventDefault(); // Prevent form submission
            toastEl.innerText = 'Payment amount cannot be greater than the total amount.';
            toastEl.classList.add('show'); // Show the toast
            setTimeout(function() {
                toastEl.classList.remove('show'); // Hide the toast after 10 seconds
            }, 10000); // 10 seconds in milliseconds
        } else if ((total - payAmt) < 100 && (total - payAmt) != 0) {
            event.preventDefault(); // Prevent form submission
            toastEl.innerText = 'Remaining amount should be at least 100.';
            toastEl.classList.add('show'); // Show the toast
            setTimeout(function() {
                toastEl.classList.remove('show'); // Hide the toast after 10 seconds
            }, 10000); // 10 seconds in milliseconds
        }
    });
});