function change_status(status) {
    var status_text = gettext("Are you sure to resume recruitment?");
    if (status == '7canceled') {
        status_text = gettext("Are you sure to cancel recruitment?");
    }
    else if (status == '8full') {
        status_text = gettext("Are you sure to finish recruitment?");
    }
    if (confirm(status_text)) {
        var url = status_url.replace(/\/1normal\//, '\/' + status +'\/');
        location.href = url;
    }
}
