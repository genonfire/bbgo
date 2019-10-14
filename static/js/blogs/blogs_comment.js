function write_comment(id) {
    content = $('#comment_text').val().replace(/\s+$/, '');
    if (content.length < 2) {
        alert(gettext("Please input 2 or more characters."));
        return;
    }

    username = $('#comment_username').val()
    if (!username || username.length == 0) {
        username = 'Guest';
    }

    var form_data = new FormData();
    form_data.append("post_id", id);
    form_data.append("comment_id", 0);
    form_data.append("content", content);
    form_data.append("username", username);

    $('body').waitMe({
        effect : 'win8',
        text : '',
        bg : 'rgba(255,255,255,0.5)',
        color : '#000'
    });

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/api/write_comment/",
        data: form_data,
        cache: false,
        contentType: false,
        processData: false,
        success: function(data) {
            $('body').waitMe('hide');
            $('#comment_text').val('');
            $('#comments').html(data);
        },
        error: function(data) {
            $('body').waitMe('hide');
            alert(gettext("Error!"));
        }
    });
}

function write_rereply(id, comment_id) {
    content = $('#rereply_text').val();
    if (content.length < 2) {
        alert(gettext("Please input 2 or more characters."));
        return;
    }

    username = $('#rereply_username').val()
    if (!username || username.length == 0) {
        username = 'Guest';
    }

    var form_data = new FormData();
    form_data.append("post_id", id);
    form_data.append("comment_id", comment_id);
    form_data.append("content", content);
    form_data.append("username", username);

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/api/write_comment/",
        data: form_data,
        cache: false,
        contentType: false,
        processData: false,
        success: function(data) {
            $('#dynamic_input_reply').remove();
            $('#comments').html(data);
        },
        error: function(data) {
            alert(gettext("Error!"));
        }
    });
}

function show_input_reply(is_authenticated, id, comment_id = 0) {
    $('#dynamic_input_reply').remove();
    body_tag = '#reply_body' + comment_id;
    placeholder = gettext("Enter comment here.");
    commentholder = gettext("Enter name here.");
    submit = gettext("submit");
    onclick_text = 'write_rereply(' + id + ', ' + comment_id + ')';
    if (is_authenticated == 'True') {
        comment_name = '';
    }
    else {
        comment_name =
        '<span class="float-left comment_name">\
            <input id="rereply_username" type="text" maxlength="' + comment_username_max + '" placeholder="' + commentholder + '">\
        </span>';
    }
    $(body_tag).append($(
    '<table id="dynamic_input_reply" class="dynamic_input_reply" width="100%">\
        <tr>\
        <td width="24px" valign="top">\
            <img src="/static/icons/niun24.png">\
        </td>\
        <td class="input_rereply">\
        <div class="input_comment">\
            <form id="form_rereply" method="post" enctype="multipart/form-data">\
                <div class="input_reply_text">\
                    <textarea id="rereply_text" maxlength="' + comment_text_max + '" placeholder="' + placeholder + '"></textarea>\
                </div>\
                <div class="input_reply_buttons">'
                    + comment_name + '<span class="float-right">\
                        <input type="button" value="' + submit + '" onClick="' + onclick_text + '">\
                    </span>\
                </div>\
            </form>\
        </div>\
    </td></tr></table>'
    ));
}

function delete_comment(id) {
    if (confirm(gettext("Are you sure to delete this comment?"))) {
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
            }
        });
        $.ajax({
            type: "POST",
            url: "/api/delete_comment/",
            data: {
                id: id
            },
            success: function(data) {
                $('#comments').html(data);
            },
            error: function(data) {
                alert(gettext('Error!'));
            }
        });
    }
}

function reload_comment(id) {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/api/reload_comment/",
        data: {
            id: id
        },
        success: function(data) {
            $('#comments').html(data);
        },
        error: function(data) {
            alert(gettext('Error!'));
        }
    });
}
