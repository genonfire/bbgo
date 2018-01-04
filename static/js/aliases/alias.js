function new_alias() {
    url = $('#original_url').val();
    if (!url || url.length < 5) {
        return;
    }
    text = gettext("Enter alias, more than 2 characters.") + "\n" + short_url + "[alias]";
    name = prompt(text);
    var pattern = /^[a-zA-Z0-9]+$/;
    if (!pattern.test(name)) {
        alert(gettext("Alphabet and number only."));
        return;
    }

    if (name && name.length >= 3 && name != 'null') {
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
            }
        });
        $.ajax({
            type: "POST",
            url: "/a/alias/new/",
            data: {
                name: name,
                url: url
            },
            success: function(data) {
                toast(gettext("Saved successfully."), 1000)
                $('#aliases').html(data);
            },
            error: function(data) {
                if (data.status == 412) {
                    toast(gettext("Exist alias. Please use different alias."));
                }
                else {
                    toast(gettext("Error!"));
                }
            }
        });
    }
    else if (name != 'null') {
        toast(gettext("Mind the chracter length limitation."), 1000);
    }
}

function edit_alias(id, url) {
    new_url = prompt(gettext("Enter original URL."), url);
    if (!new_url || new_url.length < 5) {
        return;
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/a/alias/edit/",
        data: {
            id: id,
            url: new_url
        },
        success: function(data) {
            toast(gettext("Saved successfully."), 1000)
            $('#aliases').html(data);
        },
        error: function(data) {
            if (data.status == 412) {
                toast(gettext("Not changed."));
            }
            else {
                toast(gettext("Error!"));
            }
        }
    });
}

function delete_alias(id) {
    if (confirm(gettext("Are you sure to delete?"))) {
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
            }
        });
        $.ajax({
            type: "POST",
            url: "/a/alias/delete/",
            data: {
                id: id
            },
            success: function(data) {
                $('#aliases').html(data);
            },
            error: function(data) {
                toast(gettext("Error!"));
            }
        });
    }
}
