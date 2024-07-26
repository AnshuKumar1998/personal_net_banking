document.addEventListener('DOMContentLoaded', () => {
  const eyeButton = document.getElementById('eyeButton');
  const cvvDisplay = document.getElementById('cvvDisplay');

  // Replace 'your-cvv-value' with the actual CVV value from the Django context or other source
  const cvvValue = "{{ card_details.cvv }}"; // Make sure this value is passed to the template

  eyeButton.addEventListener('click', () => {
    // Show CVV
    cvvDisplay.textContent = cvvValue;

    // Hide CVV after 10 seconds
    setTimeout(() => {
      cvvDisplay.textContent = 'xxx';
    }, 10000);
  });
});
