function delete_message(id) {
    if (confirm(gettext("Are you sure to delete this message?"))) {
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
            }
        });
        $.ajax({
            type: "POST",
            url: "/api/delete_message/",
            data: {
                id: id
            },
            success: function(data) {
                tagname = '#bubble_' + id;
                $(tagname).remove();
            },
            error: function(data) {
                alert(gettext('Error!'));
            }
        });
    }
}

$(document).ready(function() {
    $('html,body').animate({ scrollTop: $(document).height() }, 'slow');
});
