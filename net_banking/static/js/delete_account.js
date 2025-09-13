$(document).ready(function () {
    // Generate password
    $('#generatePassword').on('click', function () {
        dvloader('show');
        const username = '{{ request.user.username }}';
        const dateOfBirth = '{{ request.user.profile.date_of_birth|date:"Ymd" }}';
        const generatedPassword = username + dateOfBirth;

        $('#newPassword').val(generatedPassword);
        $('#confirmPassword').val(generatedPassword);

        setTimeout(() => {
            dvloader('hide');
        }, 200);
    });

    // Confirm Delete (with progress + logout)
    $('#confirmDelete').on('click', function () {
        closeModal();
        $('#progressOverlay').css('display', 'flex');

        fetch("{% url 'delete_account' %}", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}',
            },
            body: JSON.stringify({ username: '{{ request.user.username }}' })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'error') {
                alert(data.message);
                $('#progressOverlay').hide();
            } else {
                let progress = 0;
                const progressBar = $('#progressBar');
                const interval = setInterval(function () {
                    if (progress >= 100) {
                        clearInterval(interval);

                        fetch("{% url 'logout' %}", {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': '{{ csrf_token }}',
                            },
                        }).then(() => {
                            window.location.href = "{% url 'index' %}";
                        });
                    } else {
                        progress += 10;
                        progressBar.css('width', progress + '%');
                        progressBar.text('Processing ' + progress + '%');
                    }
                }, 500);
            }
        });
    });

    // Delete account link click (open modal)
    $('#deleteAccountLink').on('click', function (event) {
        event.preventDefault();
        $('#deleteAccountModal').show();
    });
});

// Close modal
function closeModal() {
    $('#deleteAccountModal').hide();
}

// Close change password modal
function closeChangePasswordModal() {
    $('#changePasswordModal').modal('hide');
    $('#oldPasswordSection').show();
    $('#newPasswordSection').hide();
}

// Toggle password visibility
function togglePasswordVisibility(inputId, eyeIcon) {
    const input = document.getElementById(inputId);
    const icon = eyeIcon.querySelector('i');
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}
