document.addEventListener('DOMContentLoaded', function() {
    function getCSRFToken() {
        const meta = document.querySelector('meta[name="csrf-token"]');
        if (!meta) {
            console.error("CSRF meta tag not found!");
            return '';
        }
        return meta.getAttribute('content');
    }

    document.querySelectorAll('.logout-btn').forEach(function(button) {
        button.addEventListener('click', function() {
            const userId = this.getAttribute('data-user');
            const ip = this.getAttribute('data-ip');

            fetch(`/force_logout/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({
                    user_id: userId,
                    ip_address: ip
                })
            })
            .then(response => response.json())
            .then(data => {
                if(data.status === "ok"){
                    alert(`Logout successful for IP: ${ip}`);
                    // Redirect to login page
                    window.location.href = "{% url 'login' %}";
                } else {
                    alert(`Logout failed: ${data.message}`);
                }
            })
            .catch(error => {
                console.error(error);
                alert("Something went wrong while logging out.");
            });
        });
    });
});
