function selectProfileImage() {
    $('#profileUpload').click();  // Trigger file input click event
}

$(document).ready(function() {
    $('#profileUpload').change(function() {
        var file = this.files[0];
        var formData = new FormData();
        formData.append('photo', file);
        formData.append('username', $('#username').val());  // Ensure #username exists and has a value

        // Add CSRF token
        formData.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());

       // Print "hello" to console when file is selected

        // Implement AJAX request to upload file
        $.ajax({
            type: 'POST',
            url: '/update_photo/',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                $('#profileImage').attr('src', response.photo);  // Update image source on success
            },
            error: function(xhr, status, error) {
                console.error(xhr.responseText);
            }
        });
    });
});
