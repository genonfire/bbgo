function search_reply() {
    var type = $('#search_type').val();
    var word = $('#search_word').val();
    if (!word) {
        return;
    }
    else if (word.length < 2) {
        alert(gettext("Please input 2 or more characters."));
    }
    var url = search_reply_url.replace(/type/, type).replace(/word/, word);
    location.href = url;
}

function onKeyPress(e) {
    if (e.keyCode == 13) {
        e.preventDefault();
        search_reply();
    }
}

function delete_reply(id) {
    if (confirm(gettext("Are you sure to delete this article?"))) {
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
            }
        });
        $.ajax({
            type: "POST",
            url: "/api/delete_reply/",
            data: {
                id: id
            },
            success: function(data) {
                location.reload();
            },
            error: function(data) {
                alert(gettext('Error!'));
            }
        });
    }
}

$(document).ready(function() {
    if (search_type) {
        $('#search_type').val(search_type);
    }
    if (search_word) {
        $('#search_word').val(search_word);
        if (mark_enabled) {
            $('body').mark(search_word);
        }
    }
    $(".tdlink").click(function() {
        if ($(window).width() < 768) {
            window.location = $(this).data("href");
        }
    });
});
