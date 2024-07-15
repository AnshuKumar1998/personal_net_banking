// js/statement_email_send.js

document.addEventListener('DOMContentLoaded', function() {
    const sendMailButton = document.querySelector('#sendMailButton');
    const emailInput = document.querySelector('#emailInput');
    const mailModal = document.querySelector('#mailModal');
    const successModal = document.querySelector('#successModal');

    sendMailButton.addEventListener('click', function() {
        // Fetch email from Django backend using an AJAX call
        fetch('/get_account_email/')
            .then(response => response.json())
            .then(data => {
                emailInput.value = data.email;
                // Show the modal or popup
                // Example using Bootstrap modal
                $(mailModal).modal('show');
            })
            .catch(error => console.error('Error fetching email:', error));
    });

    // Handle form submission for sending email
    const sendMailForm = document.querySelector('#sendMailForm');
    sendMailForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const email = emailInput.value.trim();
        if (email) {
            fetch('/send_mail/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ email: email })
            })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Failed to send email');
                }
            })
            .then(data => {
                console.log('Mail sent:', data);
                // Show success message or handle as needed
                $(mailModal).modal('hide');
                $(successModal).modal('show');
            })
            .catch(error => console.error('Error sending email:', error));
        }
    });

    // Function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
