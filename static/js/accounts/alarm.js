function alarm_status() {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/api/alarm_status/",
        data: {
        },
        success: function(data) {
            console.log(data[0]);
            if (data[0]) {
                $('#alarm_icon').attr('src', '/static/icons/alert24.gif');
                $('#alarm_icon_mobile').attr('src', '/static/icons/alert24.gif');
            }
            else {
                $('#alarm_icon').attr('src', '/static/icons/alert24.png');
                $('#alarm_icon_mobile').attr('src', '/static/icons/alert24.png');
            }
        },
        error: function(data) {
            alert(gettext('Error!'));
        }
    });
}

$(document).ready(function() {
    if (alarm_polling_enabled) {
        setInterval(alarm_status, alarm_polling_ms);
    }
});
