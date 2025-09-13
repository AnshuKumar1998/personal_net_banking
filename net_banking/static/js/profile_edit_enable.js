document.getElementById('profile_edit_enable').addEventListener('click', function() {
                // Enable fields for editing
                document.getElementById('name').readOnly = false;
                document.getElementById('address').readOnly = false;
                document.getElementById('gender').disabled = false;
                document.getElementById('dob').readOnly = false;
                document.getElementById('edit_submit_btn').style.display="block";
                // Change button text and disable itself
                this.disabled = true;
            });