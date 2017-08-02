function checkDuplication(check_type) {
    username = '';
    if (check_type == 'id') {
        username = $('#signup_form #id_username').val()
        if (!username || username.length < id_min_length) {
            alert(gettext("Mind the chracter length limitation."));
            return;
        }
    }
    else {
        username = $('#signup_form #id_first_name').val();
        if (!username && username.length < id_min_length) {
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
            username: username,
        },
        success: function(data) {
            alert(data.msg);
        },
        error: function(request, status, error) {
            alert(gettext("Mind the chracter length limitation."));
        }
    });
}

function checkEmail() {
    id_email = $('#signup_form #id_email').val()
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
        url: "/api/check_email/",
        data: {
            email: id_email
        },
        success: function(data) {
            alert(gettext("Verification code sent. Please check your E-mail."));
        },
        error: function(request, status, error) {
            alert(gettexxt("Failed to send E-mail. Please try again later."));
        }
    });
}

$('#signup_form').submit(function(e) {
    id_username = $('#id_username').val();
    id_nickname = $('#id_first_name').val();
    id_email = $('#id_email').val();
    id_code = $('#id_code').val();
    id_password1 = $('#id_password1').val();
    id_password2 = $('#id_password2').val();
    concent = $('#concent').is(':checked')
    if (!concent) {
        e.preventDefault();
        alert(gettext("Please consent to Terms."));
        return;
    }
    if (!id_username || !id_email || !id_password1 || !id_password2 || !id_code) {
        e.preventDefault();
        alert(gettext("Please fill all bold text which mean mandatory."));
        return;
    }
    if (id_password1 != id_password2) {
        e.preventDefault();
        alert(gettext("Passwords are different each other."));
        return;
    }
});
