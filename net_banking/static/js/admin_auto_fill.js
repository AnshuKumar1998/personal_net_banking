// static/admin/js/admin_auto_fill.js
document.addEventListener('DOMContentLoaded', function() {
    const userField = document.querySelector('#id_user');
    if (userField) {
        userField.addEventListener('change', function() {
            const userId = userField.value;
            console.log('User ID selected:', userId);  // Debugging line
            if (userId) {
                fetch(`/admin/get_user_details/?user_id=${userId}`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(data => {
                        console.log('Response:', data);  // Debugging line
                        document.querySelector('#id_username').value = data.username;
                        document.querySelector('#id_name').value = data.name;
                        document.querySelector('#id_email').value = data.email;
                        document.querySelector('#id_mobile').value = data.mobile;
                    })
                    .catch(error => {
                        console.error('Error fetching user details:', error);
                    });
            }
        });
    }
});
