function check_duplication(check_type) {
    username = '';
    if (check_type == 'id') {
        username = $('#signup_form #id_username').val();
        if (!username || username.length < id_min_length) {
            alert(gettext("Mind the chracter length limitation."));
            return;
        }
        var pattern = /^[a-zA-Z0-9._-]+$/;
        if (!pattern.test(username)) {
            alert(gettext("Alphabet Number _ - . are only available."));
            return;
        }
    }
    else {
        username = $('#signup_form #id_first_name').val();
        if (!username || username.length < nickname_min_length) {
            alert(gettext("Mind the chracter length limitation."));
            return;
        }
    }

    $.ajaxSetup({
        crossDomain: false,
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/api/check_duplication/",
        data: {
            check_type: check_type,
            username: username
        },
        success: function(data) {
            alert(data.msg);
        },
        error: function(request, status, error) {
            alert(gettext("Mind the chracter length limitation."));
        }
    });
}

function get_verification_code() {
    id_email = $('#signup_form #id_email').val();
    if (!id_email || id_email.indexOf('@') < 1) {
        alert(gettext("Please input correct E-mail address."));
        return;
    }

    $.ajaxSetup({
        crossDomain: false,
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/api/get_verification_code/",
        data: {
            email: id_email
        },
        success: function(data) {
            $('#code_hide').show();
            alert(data.msg);
        },
        error: function(request, status, error) {
            alert(gettext("Failed to send E-mail. Please try again later."));
        }
    });
}

function check_validation() {
    id_email = $('#signup_form #id_email').val();
    id_code = $('#signup_form #id_code').val();
    if (!id_code || id_code.indexOf(id_email) != 0) {
        alert(gettext("Please input verification code correctly."));
        return;
    }

    $.ajaxSetup({
        crossDomain: false,
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/api/check_validation/",
        data: {
            email: id_email,
            code: id_code
        },
        success: function(data) {
            alert(gettext("Verified successfully."));
        },
        error: function(request, status, error) {
            alert(gettext("Verification failure. Please check verification code again."));
        }
    });
}
