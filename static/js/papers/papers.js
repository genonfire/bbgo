function close_approve_box() {
    $('#approve_comment').val('');
    $('#approve_box').hide();
}

function approve_paper(id) {
    comment = $('#approve_comment').val();

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/api/approve_paper/",
        data: {
            id: id,
            comment: comment,
        },
        success: function(data) {
            close_approve_box();
            location.reload();
        },
        error: function(data) {
            if (data.status == 403) {
                toast(gettext("Please try again after reloading."))
            }
            else {
                toast(gettext("Error!"));
            }
        }
    });
}

function cancel_approve() {
    close_approve_box();
}

function approve_box() {
    $('#approve_box').show();
}

function close_reject_box() {
    $('#reject_comment').val('');
    $('#reject_box').hide();
}

function reject_paper(id) {
    comment = $('#reject_comment').val();

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/api/reject_paper/",
        data: {
            id: id,
            comment: comment,
        },
        success: function(data) {
            close_reject_box();
            location.reload();
        },
        error: function(data) {
            if (data.status == 403) {
                toast(gettext("Please try again after reloading."))
            }
            else {
                toast(gettext("Error!"));
            }
        }
    });
}

function cancel_reject() {
    close_reject_box();
}

function reject_box() {
    $('#reject_box').show();
}
