function join_team(id) {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/api/join_team/",
        data: {
            id: id
        },
        success: function(data) {
            $('#team_slot').html(data);
        },
        error: function(data) {
            if (data.status == 401) {
                toast(gettext("Require login"))
            }
            else if (data.status == 404) {
                alert(gettext("Unable to join to deleted recruitment."))
            }
            else if (data.status == 405) {
                alert(gettext("Already joined."))
            }
            else if (data.status == 406) {
                alert(gettext("Party full."))
            }
            else if (data.status == 410) {
                alert(gettext("Recruitment canceled."))
            }
            else if (data.status == 412) {
                alert(gettext("ID for this platform must exist in your user information."))
            }
            else {
                alert(gettext("Error!"));
            }
        }
    });
}

function leave_team(id) {
    if (confirm(gettext("Are you sure to leave this party?"))) {
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
            }
        });
        $.ajax({
            type: "POST",
            url: "/api/leave_team/",
            data: {
                id: id
            },
            success: function(data) {
                $('#team_slot').html(data);
            },
            error: function(data) {
                if (data.status == 401) {
                    toast(gettext("Require login"))
                }
                else if (data.status == 403) {
                    alert(gettext("Please don't leave your team behind."))
                }
                else if (data.status == 404) {
                    alert(gettext("You are not a member of this party."))
                }
                else {
                    alert(gettext("Error!"));
                }
            }
        });
    }
}

function kick_player(id, user) {
    if (confirm(gettext("Are you sure to kick this player?"))) {
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
            }
        });
        $.ajax({
            type: "POST",
            url: "/api/kick_player/",
            data: {
                id: id,
                kick_user: user
            },
            success: function(data) {
                $('#team_slot').html(data);
            },
            error: function(data) {
                if (data.status == 401) {
                    toast(gettext("Require login"))
                }
                else if (data.status == 403) {
                    alert(gettext("You are not the party leader."))
                }
                else if (data.status == 404) {
                    alert(gettext("That player is not a member of this party."))
                }
                else {
                    alert(gettext("Error!"));
                }
            }
        });
    }
}

function reload_team(id) {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/api/reload_team/",
        data: {
            id: id
        },
        success: function(data) {
            $('#team_slot').html(data);
            $('#reload_team').show();
            $('#show_new_team').hide();
        },
        error: function(data) {
            alert(gettext('Error!'));
        }
    });
}

$(document).ready(function() {
    $(".tdlink").click(function() {
        window.location = $(this).data("href");
    });
});
