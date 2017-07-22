function write_reply(id) {
    content = $('#reply_text').val();
    if (content.length < 2) {
        alert(gettext("Please input 2 or more characters."));
        return;
    }

    var form_data = new FormData();
    form_data.append("article_id", id);
    form_data.append("reply_id", 0);
    form_data.append("content", content);
    form_data.append("image", $("input[id=reply_image]")[0].files[0]);

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/api/write_reply/",
        data: form_data,
        cache: false,
        contentType: false,
        processData: false,
        success: function(data) {
            $('#reply_text').val('');
            $("#reply_image").replaceWith($("#reply_image").val('').clone(true));
            $('#replies').html(data);
        },
        error: function(data) {
            alert(gettext("Error!"));
        }
    });
}

function reload_reply(id) {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/api/reload_reply/",
        data: {
            id: id
        },
        success: function(data) {
            $('#replies').html(data);
        },
        error: function(data) {
            alert(gettext('Error!'));
        }
    });
}

$('#reply_image').on('change', function() {
    var file = this.files[0];
    if (file.size > reply_image_limit) {
        var sizelimit = reply_image_limit / 1024 / 1024 + 'MB';
        msg = gettext("Selected image is too big. size limit: ") + sizelimit;
        $("#reply_image").replaceWith($("#reply_image").val('').clone(true));
        alert(msg);
    }
});
