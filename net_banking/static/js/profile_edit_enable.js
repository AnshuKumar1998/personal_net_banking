document.getElementById('editButton').addEventListener('click', function() {
                // Enable fields for editing
                document.getElementById('name').readOnly = false;
                document.getElementById('address').readOnly = false;
                document.getElementById('gender').disabled = false;
                document.getElementById('dob').readOnly = false;

                // Change button text and disable itself
                this.disabled = true;
            });