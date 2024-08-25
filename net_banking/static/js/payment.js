function togglePaymentOption(option) {
    var paymentAmountInput = document.getElementById("payment_amount");
    var depositeAmount = parseFloat(document.getElementById("deposite_amount").innerText.trim());

    // Assuming the text in the "month" element is something like "Monthly: 100"
    var perMonthText = document.getElementById("month").innerText.trim();
    var perMonthAmount = parseFloat(perMonthText.split(" ")[1]); // Get only the amount value

    if (option === 'full') {
        document.getElementById("emi_radio").checked = false;
        paymentAmountInput.value = depositeAmount.toFixed(2);
    } else if (option === 'emi') {
        document.getElementById("full_payment_radio").checked = false;
        paymentAmountInput.value = perMonthAmount.toFixed(2);
    }
}
