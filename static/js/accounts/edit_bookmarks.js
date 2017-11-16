function delete_li(id) {
    $('#' + id).remove();
}

$('#edit_bookmarks_form').submit(function(e) {
    e.preventDefault();
    bookmarks = [""];

    $('#sort_items li').each(function(i) {
        id = $(this).attr('id');
        bookmarks.push(id);
    });

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/api/edit_bookmarks/",
        data: {
            bookmarks: bookmarks
        },
        success: function(data) {
            $('#result_msg').html(data[0]);
        },
        error: function(data) {
            alert(gettext('Error!'));
        }
    });
});

$(function() {
    $("#sort_items").sortable({containment: "#sort_container"});
    $("#sort_items").disableSelection();
});
