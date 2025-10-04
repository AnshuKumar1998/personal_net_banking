document.addEventListener('DOMContentLoaded', function() {

    const header = document.getElementById('action-header');
    const content = document.getElementById('content');
    const modal = new bootstrap.Modal(document.getElementById('actionModal'));
    const modalTitle = document.getElementById('actionModalLabel');
    const modalBody = document.querySelector('.modal-body');

    document.querySelectorAll('.read-more').forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const actionId = this.getAttribute('data-id');

            // Fetch action details (assuming you have an endpoint for this)
            fetch(`/action/${actionId}/`)
                .then(response => response.json())
                .then(data => {
                    modalTitle.textContent = data.subject;
                    modalBody.textContent = data.content;
                    modal.show();
                    setTimeout(() => {
                        dvloader('hide');
                    }, 400);
                })
                .catch(error => console.error('Error fetching action details:', error));
        });
    });


    const newActionLink = document.getElementById('new-action-link');
    if(newActionLink){
        newActionLink.addEventListener('click', function() {
            header.innerText = 'Action Center';
            filterActions('new');
        });
    }


    const pendingActionLink = document.getElementById('pending-action-link');
    if(pendingActionLink){
        pendingActionLink.addEventListener('click', function() {
            header.innerText = 'Pending Action';
            filterActions('pending');
        });
    }


    const completedActionLink = document.getElementById('completed-action-link');
    if(completedActionLink){
         completedActionLink.addEventListener('click', function() {
            header.innerText = 'Completed Action';
            filterActions('completed');
        });
    }


    const blockActionLink = document.getElementById('block-action-link');
    if(blockActionLink){
        blockActionLink.addEventListener('click', function() {
            header.innerText = 'Block Action';
            filterActions('blocked');
        });
    }



    function filterActions(status) {
        document.querySelectorAll('.action-item').forEach(item => {
            if (item.getAttribute('data-status') === status) {
                item.style.display = 'block';
            } else {
                item.style.display = 'none';
            }
        });
    }


});

document.addEventListener("DOMContentLoaded", function() {
    const doLaterButtons = document.querySelectorAll(".do-later-btn");

    doLaterButtons.forEach(button => {
        button.addEventListener("click", function() {

            const actionId = this.dataset.id;
            const actionItem = this.closest(".action-item");

            fetch(`/action/do_later/${actionId}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie('csrftoken')  // CSRF token important hai
                },
                body: JSON.stringify({ status: "pending" })
            })
            .then(response => response.json())
            .then(data => {
                if(data.success) {
                    // Remove from new actions
                    actionItem.remove();
                } else {
                    alert("Error marking action as pending!");
                }
            });
        });
    });

    // CSRF helper
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
});

document.addEventListener("DOMContentLoaded", function() {
    attachDoLaterEvents();

    function attachDoLaterEvents() {
        const doLaterButtons = document.querySelectorAll(".do-later-btn");

        doLaterButtons.forEach(button => {
            button.addEventListener("click", function() {
                const actionId = this.dataset.id;
                const actionItem = this.closest(".action-item");

                fetch(`/action/do_later/${actionId}/`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCookie("csrftoken")
                    },
                    body: JSON.stringify({ status: "pending" })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // ✅ Remove from New Actions
                        actionItem.remove();

                        // ✅ Move to Pending Actions section
                        const pendingSection = document.getElementById("pending-actions");
                        pendingSection.appendChild(actionItem);

                        // ✅ Update status
                        actionItem.dataset.status = "pending";

                        // ✅ Update expire-date color
                        const expireText = actionItem.querySelector(".expire-date");
                        if (expireText) {
                            expireText.className = "expire-date pending";
                            expireText.style.color = "red";
                        }

                        // ✅ Remove Do Later button in pending list
                        const btn = actionItem.querySelector(".do-later-btn");
                        if (btn) btn.remove();
                    } else {
                        alert("Error updating action!");
                    }
                });
            });
        });
    }

    // Helper: CSRF token getter
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
});







