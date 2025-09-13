document.addEventListener('DOMContentLoaded', function () {
    var toastEl = document.getElementById('toastMessage');
    var paymentForm = document.getElementById('paymentForm');
    // Safely get total from Django
    var total = {{ total|default:0 }};  // Agar total empty ho to 0

    // Null check for form
    if (paymentForm) {
        paymentForm.addEventListener('submit', function(event) {
            var payAmtInput = document.getElementById('pay_amt');
            if (!payAmtInput) return; // Input missing

            var payAmt = parseFloat(payAmtInput.value) || 0;

            if (payAmt > total) {
                event.preventDefault();
                toastEl.innerText = 'Payment amount cannot be greater than the total amount.';
                toastEl.classList.add('show');
                setTimeout(function() {
                    toastEl.classList.remove('show');
                }, 10000);
            } else if ((total - payAmt) < 100 && (total - payAmt) !== 0) {
                event.preventDefault();
                toastEl.innerText = 'Remaining amount should be at least 100.';
                toastEl.classList.add('show');
                setTimeout(function() {
                    toastEl.classList.remove('show');
                }, 10000);
            }
        });
    }
});
