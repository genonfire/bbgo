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
            if (data[0]) {
                $('#alarm_icon').attr('src', '/static/icons/alert24.gif');
                $('#alarm_icon_mobile').attr('src', '/static/icons/alert24.gif');

                var options = {
                    title: site_name,
                    options: {
                        body: gettext("Alarm for your activity."),
                        icon: site_logo,
                        lang: 'ko-KR'
                    }
                };
                $("#easyNotify").easyNotify(options);
            }
            else {
                $('#alarm_icon').attr('src', '/static/icons/alert24.png');
                $('#alarm_icon_mobile').attr('src', '/static/icons/alert24.png');
            }
        },
        error: function(data) {
            // alert(gettext('Error!'));
        }
    });
}

function clear_alarm(type) {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/api/clear_alarm/",
        data: {
        },
        success: function(data) {
            alarm_list(type);
        },
        error: function(data) {
            alert(gettext('Error!'));
        }
    });
}

function alarm_list(type) {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/api/alarm_list/",
        data: {
            type: type,
        },
        success: function(data) {
            if (type == 'desktop') {
                $('#alarm_list').html(data);
                $('#alarm_list').show();
                $('#alarm_icon').attr('src', '/static/icons/alert24.png');

                $('#alarm_list').on('mousedown touchstart', function(e) {
                    e.stopPropagation();
                })
                $('body').on('mousedown touchstart', function(e) {
                    $('#alarm_list').hide();
                    $('body').off('mousedown touchstart');
                })
            }
            else if (type == 'mobile') {
                $('html,body').animate({ scrollTop: 0 }, 'slow');
                $('#alarm_list_mobile').html(data);
                $('#alarm_list_mobile').show();
                $('#alarm_icon_mobile').attr('src', '/static/icons/alert24.png');

                $('#alarm_list_mobile').on('mousedown touchstart', function(e) {
                    e.stopPropagation();
                })
                $('body').on('mousedown touchstart', function(e) {
                    $('#alarm_list_mobile').hide();
                    $('body').off('mousedown touchstart');
                })
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
