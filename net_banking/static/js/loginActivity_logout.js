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
            dvloader('show');
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
                    dvloader('hide');
                    window.location.href = "{% url 'login' %}";
                } else {
                    dvloader('hide');
                    alert(`Logout failed: ${data.message}`);
                }
            })
            .catch(error => {
                dvloader('hide');
                console.error(error);
                alert("Something went wrong while logging out.");
            });
        });
    });
});



let ipToBlock = null;

document.querySelectorAll('.block-ip-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        ipToBlock = this.getAttribute('data-ip');
        document.getElementById('ip-to-block').innerText = ipToBlock;
        let modal = new bootstrap.Modal(document.getElementById('blockIpModal'));
        modal.show();
    });
});

document.getElementById('confirmBlockBtn').addEventListener('click', function() {
    if(ipToBlock){
        dvloader('show');
        fetch(`/loginactivity/block/${ipToBlock}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie('csrftoken')  // CSRF token important hai
            },
            body: JSON.stringify({ status: "block" })
        })
        .then(response => response.json())
        .then(data => {
            if(data.success) {
                dvloader('hide');
                let msgDiv = document.getElementById("block-list-msg");
                msgDiv.innerHTML = `<div class="alert alert-success mb-2">IP Blocked Successfully</div>`;

            } else {
                dvloader('hide');
                alert("Error marking block !");
            }
        });
        $('#blockIpModal').modal('hide');
    }
});

$('#blockIpModal').on('hidden.bs.modal', function () {
    location.reload();
});


function closeBlockIPModal() {
    $('#blockIpModal').modal('hide');
     setTimeout(() => {
        document.body.focus();
    }, 200);
}
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.getElementById("showBlockedBtn").addEventListener("click", function() {
    dvloader('show');
    fetch("/loginactivity/blocked/")
        .then(res => res.json())
        .then(data => {
            let tbody = document.getElementById("blocked-list-body");
            let msgDiv = document.getElementById("blocked-list-msg");
            msgDiv.innerHTML = ""; // clear previous messages
            tbody.innerHTML = "";

            if (data.length > 0) {
                data.forEach((item, index) => {
                    tbody.innerHTML += `
                        <tr>
                            <td>${index + 1}</td>
                            <td>${item.username || "UNKNOWN"}</td>
                            <td>${item.ip_address}</td>
                            <td>${item.device_type}</td>
                            <td>${item.browser}</td>
                            <td>${item.created_at}</td>
                            <td>
                                <button class="btn btn-success btn-sm unblock-btn" data-ip="${item.ip_address}">Unblock</button>
                            </td>
                        </tr>
                    `;
                });

                // 🔥 Add unblock button event
                tbody.querySelectorAll(".unblock-btn").forEach(btn => {
                    btn.addEventListener("click", function() {
                        let ip = this.dataset.ip;
                        fetch(`/loginactivity/unblock/${ip}/`, {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                                "X-CSRFToken": getCookie('csrftoken')
                            },
                            body: JSON.stringify({ status: "unblock" })
                        })
                        .then(r => r.json())
                        .then(resp => {
                            if (resp.success) {
                                // ✅ Modal ke andar success message
                                msgDiv.innerHTML = `<div class="alert alert-success mb-2">${resp.message}</div>`;
                                // Remove row from table
                                this.closest("tr").remove();

                                // Agar list empty ho gayi to message dikhaye
                                if(tbody.children.length === 0) {
                                    tbody.innerHTML = `<tr><td colspan="7" class="text-center">No blocked IPs found</td></tr>`;
                                }
                            } else {
                                msgDiv.innerHTML = `<div class="alert alert-danger mb-2">${resp.message}</div>`;
                            }
                        });
                    });
                });
                dvloader('hide');
            } else {

                tbody.innerHTML = `<tr><td colspan="7" class="text-center">No blocked IPs found</td></tr>`;
                dvloader('hide');
            }

            // Show modal
            $('#blockedListModal').modal('show');
        });
});
