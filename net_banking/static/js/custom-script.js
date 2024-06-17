$(document).ready(function() {
    {% if messages %}
        $('#successModal').modal('show');
    {% endif %}
});
