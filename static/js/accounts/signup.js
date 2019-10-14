$('#signup_form').submit(function(e) {
    id_username = $('#signup_form #id_username').val();
    id_nickname = $('#signup_form #id_first_name').val();
    if (!id_username || id_username.length < id_min_length) {
        e.preventDefault();
        alert(gettext("Mind the chracter length limitation."));
        return;
    }
    if (id_nickname && id_nickname.length < nickname_min_length) {
        e.preventDefault();
        alert(gettext("Mind the chracter length limitation."));
        return;
    }

    id_email = $('#signup_form #id_email').val();
    id_code = $('#signup_form #id_code').val();
    id_password1 = $('#signup_form #id_password1').val();
    id_password2 = $('#signup_form #id_password2').val();
    if (!id_email || !id_password1 || !id_password2 || !id_code) {
        e.preventDefault();
        alert(gettext("Please fill all bold text which mean mandatory."));
        return;
    }
    if (id_password1 != id_password2) {
        e.preventDefault();
        alert(gettext("Passwords are different each other."));
        return;
    }

    concent = $('#concent').is(':checked')
    if (!concent) {
        e.preventDefault();
        alert(gettext("Please consent to Terms."));
        return;
    }
});
