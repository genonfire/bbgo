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

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/api/write_team_reply/",
        data: form_data,
        cache: false,
        contentType: false,
        processData: false,
        success: function(data) {
            $('#reply_text').val('');
            $('#replies').html(data);
        },
        error: function(data) {
            if (data.status == 401) {
                alert(gettext("Require login"))
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

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/api/write_team_reply/",
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
                <div class="input_reply_buttons">' + 
                    '<span class="float-right">\
                        <input type="button" value="' + submit + '" onClick="' + onclick_text + '">\
                    </span>\
                </div>\
            </form>\
        </div>\
    </td></tr></table>'
    ));
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
            url: "/api/delete_team_reply/",
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
        url: "/api/reload_team_reply/",
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
        url: "/api/team_reply_count/",
        data: {
            id: article_id
        },
        success: function(data) {
            new_replies = data[0] - reply_count;
            new_slot = data[1] - slot_in;
            if (new_replies > 0) {
                $('#reload_reply').hide();
                newtext = gettext("Show new replies") + ': ' + new_replies;
                $('#show_new_reply a').text(newtext);
                $('#show_new_reply').show();
            }
            if (new_slot != 0) {
                $('#reload_team').hide();
                newtext = gettext("Show new guardians") + ': ' + new_slot;
                $('#show_new_team a').text(newtext);
                $('#show_new_team').show();
            }
        },
        error: function(data) {
            alert(gettext('Error!'));
        }
    });
}

$(document).ready(function() {
    if (reply_auto_renew_enabled) {
        setInterval(get_reply_no, reply_auto_renew_ms);
    }
});
