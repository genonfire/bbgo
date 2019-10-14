function search_person() {
    var type = $('#edit_paper_form input[name=line_type]:checked').val();
    var name = $('#line_name').val();

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/api/user_by_name/",
        data: {
            type: type,
            name: name,
            blacklist: blacklist,
        },
        success: function(data) {
            if (data.status == 'only') {
                select_person(
                    data.type, data.id, data.username, data.name, data.email);
            }
            else {
                $('#name_list').html(data);
                $('#name_list').show();
            }
        },
        error: function(data) {
            toast(gettext("Error!"));
        }
    });
}

function select_person(type, id, username, name, email) {
    var is_approval = false;
    var is_support = false;
    if (name == '')
        name = username;
    blacklist.push(username);

    switch(type) {
        case "approver":
            type_text = gettext("Approval");
            $('#supporter_button').prop('checked', true);
            $('#approver_button').prop('disabled', true);
            is_approval = true;
            break;
        case "supporter":
            type_text = gettext("Support");
            is_support = true;
            break;
        case "notifier":
            type_text = gettext("Notify");
            break;
    }

    var func_name = 'delete_this_thing';
    if (is_approval)
        var func_name = 'delete_this_approval';
    else if (is_support)
        var func_name = 'delete_this_support';

    li_id = "li_id_" + username;
    li_text = '<li id="' + li_id + '" class="' + type + '"><span>' + type_text + '</span>' + name + ' / ' + email + ' <a href=javascript:' + func_name + '("' + username + '")><img src="/static/icons/delete10.png"></a></li>';

    if (is_approval) {
        $('#id_approver').val(id);
        $('li.proposer').after(li_text);
    }
    else if (is_support) {
        names = $('#id_support_names').val();
        if (names == '')
            $('#id_support_names').val(username);
        else
            $('#id_support_names').val(names + ',' + username);
        $('.line_names ul').append(li_text);
    }
    else {
        names = $('#id_notify_names').val();
        if (names == '')
            $('#id_notify_names').val(username);
        else
            $('#id_notify_names').val(names + ',' + username);
        $('.line_names ul').append(li_text);
    }

    $('#name_list').hide();
    $('#line_name').val('');
}

function delete_this_li(name) {
    $('#li_id_' + name).remove();

    var index = blacklist.indexOf(name);
    if (index != -1)
        blacklist.splice(index, 1);
}

function delete_this_approval(name) {
    delete_this_li(name);
    $('#id_approver').val('');
    $('#approver_button').prop('disabled', false);
    $('#approver_button').prop('checked', true);
}

function delete_this_support(name) {
    delete_this_li(name);
    names = $('#id_support_names').val().split(',');
    var index = names.indexOf(name);
    if (index != -1)
        names.splice(index, 1);
    $('#id_support_names').val(names);
}

function delete_this_notify(name) {
    delete_this_li(name);
    names = $('#id_notify_names').val().split(',');
    var index = names.indexOf(name);
    if (index != -1)
        names.splice(index, 1);
    $('#id_notify_names').val(names);
}

function list_cancel() {
    $('#name_list').hide();
}

function onKeyPress(e) {
    if (e.keyCode == 13) {
        e.preventDefault();
        search_person();
    }
}

$('#edit_paper_form').submit(function(e) {
    approver = $('#id_approver').val();
    if (!approver || approver == '') {
        e.preventDefault();
        alert(gettext('Approver is necessary.'));
        return;
    }

    if (confirm(gettext("Are you sure to make a proposal?"))) {
        $(window).off('beforeunload');
    }
    else {
        e.preventDefault();
        return;
    }
})

$(window).on('beforeunload', function(){
    return gettext('Are you sure to quit editing?');
});
