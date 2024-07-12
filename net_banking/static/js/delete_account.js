
       $('#generatePassword').on('click', function() {
           const username = '{{ request.user.username }}';
           const dateOfBirth = '{{ request.user.profile.date_of_birth|date:"Ymd" }}'; // Assuming the user profile has a date_of_birth field
           const generatedPassword = username + dateOfBirth;

           $('#newPassword').val(generatedPassword);
           $('#confirmPassword').val(generatedPassword);
       });

       $('#confirmDelete').on('click', function() {
           closeModal();
           $('#progressOverlay').show();

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
                   const interval = setInterval(function() {
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
                           progressBar.width(progress + '%');
                           progressBar.text('Processing ' + progress + '%');
                       }
                   }, 500);
               }
           });
       });

       function closeModal() {
           $('#deleteAccountModal').modal('hide');
       }

       function closeChangePasswordModal() {
           $('#changePasswordModal').modal('hide');
           $('#oldPasswordSection').show();
           $('#newPasswordSection').hide();
       }
   });

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

    document.getElementById('deleteAccountLink').addEventListener('click', function(event) {
        event.preventDefault();
        document.getElementById('deleteAccountModal').style.display = 'block';
    });

    document.getElementById('confirmDelete').addEventListener('click', function() {
        // Hide the modal
        closeModal();

        // Show progress overlay
        document.getElementById('progressOverlay').style.display = 'flex';

        // Make AJAX call to delete account
        fetch("{% url 'delete_account' %}", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}',
            },
            body: JSON.stringify({
                username: '{{ request.user.username }}'
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'error') {
                alert(data.message);
                document.getElementById('progressOverlay').style.display = 'none';
            } else {
                let progress = 0;
                const progressBar = document.getElementById('progressBar');
                const interval = setInterval(function() {
                    if (progress >= 100) {
                        clearInterval(interval);
                        // Log out the user
                        fetch("{% url 'logout' %}", {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': '{{ csrf_token }}',
                            },
                        }).then(() => {
                            // Redirect to index page after completion
                            window.location.href = "{% url 'index' %}";
                        });
                    } else {
                        progress += 10;
                        progressBar.style.width = progress + '%';
                        progressBar.innerText = 'Processing ' + progress + '%';
                    }
                }, 500);
            }
        });
    });

    function closeModal() {
        document.getElementById('deleteAccountModal').style.display = 'none';
    }

    #progressOverlay {
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: 9999;
        justify-content: center;
        align-items: center;
    }

    #progressContainer {
        width: 300px;
        padding: 20px;
        border-radius: 10px;
    }

    .progress {
        border-radius: 10px;
    }
