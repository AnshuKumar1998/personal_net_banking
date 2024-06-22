// static/js/post_pagination.js

$(document).ready(function() {
    $('.like-btn').click(function() {
        var postId = $(this).data('post-id');
        $.ajax({
            url: '/like/' + postId + '/',
            method: 'POST',
            data: {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(response) {
                $('#like-count-' + postId).text(response.likes);
            }
        });
    });
});
