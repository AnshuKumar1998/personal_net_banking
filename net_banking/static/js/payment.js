<script>
function togglePaymentOption(option) {
    var paymentAmount = document.getElementById("payment_amount");
    var depositeAmount = document.getElementById("deposite_amount").innerText;
    var perMonthAmount = document.getElementById("month").innerText.split(" ")[1]; // Get only the amount value

    if (option === 'full') {
        document.getElementById("emi_checkbox").checked = false;
        paymentAmount.value = depositeAmount;
    } else if (option === 'emi') {
        document.getElementById("full_payment_checkbox").checked = false;
        paymentAmount.value = perMonthAmount;
    }
}

function processPayment() {
    var isAuthenticated = JSON.parse(document.getElementById("is_authenticated").innerText);
    if (!isAuthenticated) {
        alert("You need to log in to make a payment.");
        return;
    }

    // Submit the form via AJAX
    var form = document.getElementById("paymentForm");
    var formData = new FormData(form);

    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            $('#successModal').modal('show');
        } else {
            alert("There was an error processing your payment. Please try again.");
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("There was an error processing your payment. Please try again.");
    });
}

function redirectToFixDepositList() {
    // Hardcode the URL path
    var fixDepositListUrl = "/service/fix_deposit_list/";
    window.location.href = fixDepositListUrl;
}

</script>