function togglePaymentOption(option) {
    var paymentAmountInput = document.getElementById("payment_amount");
    var depositeAmount = parseFloat(document.getElementById("deposite_amount").innerText.trim());
    var perMonthAmount = parseFloat(document.getElementById("month").innerText.trim().split(" ")[1]); // Get only the amount value

    if (option === 'full') {
        document.getElementById("emi_radio").checked = false;
        paymentAmountInput.value = depositeAmount.toFixed(2);
    } else if (option === 'emi') {
        document.getElementById("full_payment_radio").checked = false;
        paymentAmountInput.value = perMonthAmount.toFixed(2);
    }
}
