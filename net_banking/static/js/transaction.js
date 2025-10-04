// Fetch transaction months and populate the delete form
function openDeletePopup() {
    fetch('/fetch-transaction-months/')
        .then(response => response.json())
        .then(data => {
            const deleteForm = document.getElementById('deleteForm');
            deleteForm.innerHTML = '';

            data.months.forEach(month => {
                const checkboxContainer = document.createElement('div');
                checkboxContainer.classList.add('checkbox-container');

                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.name = 'months';
                checkbox.value = month;
                checkbox.id = month;

                const label = document.createElement('label');
                label.htmlFor = month;
                label.innerText = month;
                label.style.marginLeft = '10px';  // Add margin to create space

                checkboxContainer.appendChild(checkbox);
                checkboxContainer.appendChild(label);

                deleteForm.appendChild(checkboxContainer);
            });

            $('#deleteModal').modal('show');
        })
        .catch(error => console.error('Error fetching transaction months:', error));
}

// Delete selected transactions
function deleteTransactions() {
    const form = document.getElementById('deleteForm');
    const formData = new FormData(form);
    const selectedMonths = formData.getAll('months');

    if (selectedMonths.length === 0) {
        alert('Please select at least one month to delete.');
        return;
    }

    fetch('/delete-transactions/', {
        method: 'POST',
        body: JSON.stringify({ months: selectedMonths }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Transactions deleted successfully.');
            $('#deleteModal').modal('hide');
            location.reload(); // Refresh the page to reflect changes
        } else {
            alert('Error deleting transactions.');
        }
    })
    .catch(error => console.error('Error deleting transactions:', error));
}

// Utility function to get the CSRF token
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


function openExportModal() {
    const exportModal = new bootstrap.Modal(document.getElementById('exportModal'));
    exportModal.show();
}

function downloadStatement(format) {
    const params = new URLSearchParams(window.location.search);
    params.append('format', format);
    params.append('password', 'admin'); // default password

    // Open export link in new tab
    window.location.href = `/export-transaction-statement/?${params.toString()}`;
}

function printStatement() {
    const printContents = document.getElementById('printableArea').innerHTML;
    const originalContents = document.body.innerHTML;

    document.body.innerHTML = printContents;
    window.print();
    document.body.innerHTML = originalContents;
    location.reload();
}


