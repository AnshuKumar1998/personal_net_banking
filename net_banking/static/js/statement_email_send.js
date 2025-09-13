document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const sendMailButton = document.querySelector('#sendMailButton');
    const emailInput = document.querySelector('#emailInput');
    const mailModal = document.querySelector('#mailModal');
    const successModal = document.querySelector('#successModal');
    const sendMailForm = document.querySelector('#sendMailForm');

    // Ensure all required elements exist
    if (sendMailButton && emailInput && mailModal && sendMailForm) {

        // Fetch user email and show modal
        const sendMailButton = document.querySelector('#sendMailButton');
        if (sendMailButton) {
             sendMailButton.addEventListener('click', function() {
             fetch('/get_account_email/')
                .then(response => response.json())
                .then(data => {
                    emailInput.value = data.email || '';
                    $(mailModal).modal('show'); // Bootstrap modal
                })
                .catch(error => console.error('Error fetching email:', error));
             });

        }


        // Handle email form submission

        sendMailForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const email = emailInput.value.trim();
            if (!email) return;

            if (typeof dvloader === 'function') dvloader('show');

            fetch('/send_mail/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ email: email })
            })
            .then(response => response.ok ? response.json() : Promise.reject('Failed to send email'))
            .then(data => {
                console.log('Mail sent:', data);
                $(mailModal).modal('hide');
                $(successModal).modal('show');
            })
            .catch(error => console.error('Error sending email:', error))
            .finally(() => {
                if (typeof dvloader === 'function') dvloader('hide');
            });
        });
    }

    // Helper function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
