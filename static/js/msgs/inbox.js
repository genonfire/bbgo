function delete_all() {
    if (confirm(gettext("Are you sure to delete all?"))) {
        location.href = delete_all_url;
    }
}

function delete_old() {
    if (confirm(gettext("Are you sure to delete old messages?"))) {
        location.href = delete_old_url;
    }
}

function delete_conversation(user) {
    if (confirm(gettext("Are you sure to delete this conversation?"))) {
        url = delete_converation_url.replace(/\/bb\//, '\/' + user +'\/');
        location.href = url;
    }
}
