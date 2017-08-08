function deactivate_account(url) {
    concent = $('#concent').is(':checked')
    if (!concent) {
        alert(gettext("Please consent to Terms."));
        return;
    }
    else {
        if (confirm(gettext("Are you sure to delete your profile?"))) {
            location.href = url;
        }
    }
}
