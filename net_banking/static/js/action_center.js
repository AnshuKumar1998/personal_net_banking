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
                })
                .catch(error => console.error('Error fetching action details:', error));
        });
    });

    document.getElementById('new-action-link').addEventListener('click', function() {
        header.innerText = 'Action Center';
        filterActions('new');
    });

    document.getElementById('pending-action-link').addEventListener('click', function() {
        header.innerText = 'Pending Action';
        filterActions('pending');
    });

    document.getElementById('completed-action-link').addEventListener('click', function() {
        header.innerText = 'Completed Action';
        filterActions('completed');
    });

    document.getElementById('block-action-link').addEventListener('click', function() {
        header.innerText = 'Block Action';
        filterActions('blocked');
    });

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



