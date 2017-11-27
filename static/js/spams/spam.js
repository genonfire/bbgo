function add_ip() {
    ip = $('#spam_ip').val()
    if (ip.length < 7) {
        alert(gettext("Please input correct IP address."));
        return;
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/spams/add_ip/",
        data: {
            ip: ip
        },
        success: function(data) {
            $('#spam_ips').html(data);
        },
        error: function(data) {
            if (data.status == 412) {
                alert(gettext("Already exist."))
            }
            else if (data.status == 500) {
                alert(gettext("Please input correct IP address."));
            }
        }
    });
}

function delete_ip(id) {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/spams/delete_ip/",
        data: {
            id: id
        },
        success: function(data) {
            $('#spam_ips').html(data);
        },
    });
}

function add_word() {
    word = $('#spam_word').val()
    if (word.length < 2) {
        alert(gettext("Please input 2 or more characters."));
        return;
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/spams/add_word/",
        data: {
            word: word
        },
        success: function(data) {
            $('#spam_words').html(data);
        },
        error: function(data) {
            if (data.status == 412) {
                alert(gettext("Already exist."))
            }
        }
    });
}

function delete_word(id) {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/spams/delete_word/",
        data: {
            id: id
        },
        success: function(data) {
            $('#spam_words').html(data);
        },
    });
}
