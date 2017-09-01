function write_reply(id) {
    content = $('#reply_text').val().replace(/\s+$/, '');
    if (content.length < 2) {
        alert(gettext("Please input 2 or more characters."));
        return;
    }

    var form_data = new FormData();
    form_data.append("article_id", id);
    form_data.append("reply_id", 0);
    form_data.append("content", content);
    if (reply_image_available) {
        form_data.append("image", $("input[id=reply_image]")[0].files[0]);
    }

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
            if (data.status == 401) {
                alert(gettext("Require login"))
            }
            else if (data.status == 402) {
                alert(gettext("Reply to warning article is not available."))
            }
            else {
                alert(gettext("Error!"));
            }
        }
    });
}

function write_rereply(id, reply_id) {
    content = $('#rereply_text').val();
    if (content.length < 2) {
        alert(gettext("Please input 2 or more characters."));
        return;
    }

    var form_data = new FormData();
    form_data.append("article_id", id);
    form_data.append("reply_id", reply_id);
    form_data.append("content", content);
    if (reply_image_available) {
        form_data.append("image", $("input[id=rereply_image]")[0].files[0]);
    }

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
            $('#dynamic_input_reply').remove();
            $('#replies').html(data);
        },
        error: function(data) {
            alert(gettext("Error!"));
        }
    });
}

function show_input_reply(id, reply_id = 0) {
    $('#dynamic_input_reply').remove();
    body_tag = '#reply_body' + reply_id;
    placeholder = gettext("Please show some respect.");
    submit = gettext("submit");
    onclick_text = 'write_rereply(' + id + ', ' + reply_id + ')';
    if (reply_image_available) {
        reply_image =
        '<span>\
            <input id="rereply_image" type="file" accept="image/*">\
        </span>'
    }
    else {
        reply_image = ''
    }
    $(body_tag).append($(
    '<table id="dynamic_input_reply" class="dynamic_input_reply" width="100%">\
        <tr>\
        <td width="24px" valign="top">\
            <img src="/static/icons/niun24.png">\
        </td>\
        <td class="input_rereply">\
        <div class="input_reply">\
            <form id="form_rereply" method="post" enctype="multipart/form-data">\
                <div class="input_reply_text">\
                    <textarea id="rereply_text" maxlength="' + reply_text_max + '"\ placeholder="' + placeholder + '"></textarea>\
                </div>\
                <div class="input_reply_buttons">'
                    + reply_image +
                    '<span class="float-right">\
                        <input type="button" value="' + submit + '" onClick="' + onclick_text + '">\
                    </span>\
                </div>\
            </form>\
        </div>\
    </td></tr></table>'
    ));

    if (reply_image_available) {
        $('#rereply_image').on('change', function() {
            var file = this.files[0];
            if (file.size > reply_image_limit) {
                var sizelimit = reply_image_limit / 1024 / 1024 + 'MB';
                msg = gettext("Selected image is too big. size limit: ") + sizelimit;
                $("#rereply_image").replaceWith($("#rereply_image").val('').clone(true));
                alert(msg);
            }
        });
    }
}

function like_reply(id) {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/api/like_reply/",
        data: {
            id: id
        },
        success: function(data) {
            if (data[0] == 0) {
                alert(data[1]);
                return;
            }
            tagname = '#thumb_up_msg' + id;
            $(tagname).html(data[0]);
        },
        error: function(data) {
            alert(gettext('Error!'));
        }
    });
}

function dislike_reply(id) {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/api/dislike_reply/",
        data: {
            id: id
        },
        success: function(data) {
            if (data[0] == 0) {
                alert(data[1]);
                return;
            }
            tagname = '#thumb_down_msg' + id;
            $(tagname).html(data[0]);
        },
        error: function(data) {
            alert(gettext('Error!'));
        }
    });
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
                $('#replies').html(data);
            },
            error: function(data) {
                alert(gettext('Error!'));
            }
        });
    }
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
            $('#reload_reply').show();
            $('#show_new_reply').hide();
        },
        error: function(data) {
            alert(gettext('Error!'));
        }
    });
}

function get_reply_no() {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/api/reply_count/",
        data: {
            id: article_id
        },
        success: function(data) {
            new_replies = data[0] - reply_count;
            if (new_replies > 0) {
                $('#reload_reply').hide();
                newtext = gettext("Show new replies") + ': ' + new_replies;
                $('#show_new_reply a').text(newtext);
                $('#show_new_reply').show();
            }
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

$(document).ready(function() {
    if (reply_auto_renew_enabled) {
        setInterval(get_reply_no, reply_auto_renew_ms);
    }
});
