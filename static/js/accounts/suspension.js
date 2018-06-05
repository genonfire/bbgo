function suspend(userinfo) {
    user = userinfo;
    days = $('#suspension_days').val();
    if (!days || days == 0) {
        alert(gettext("Number only!"));
        return;
    }

    var pattern = /^[0-9]+$/;
    if (!pattern.test(days)) {
        alert(gettext("Number only!"));
        return;
    }

    url = "/accounts/suspension/" + user + "/" + days + "/";

    if (confirm(gettext("Are you sure to discipline?"))) {
        location.href = url;
    }
}

function clear_suspension(userinfo) {
    user = userinfo;
    url = "/accounts/suspension/" + user + "/0/";

    if (confirm(gettext("Clear suspension?"))) {
        location.href = url;
    }
}
