function like_article(id) {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/api/like_article/",
        data: {
            id: id
        },
        success: function(data) {
            $('#article_view_text').html(data[1]);
            if (data[0] > 0) {
                $('#article_view_like_count').html(data[0]);
            }
        },
        error: function(data) {
            $('#article_view_text').html('error');
        }
    });
}

function dislike_article(id) {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/api/dislike_article/",
        data: {
            id: id
        },
        success: function(data) {
            $('#article_view_text').html(data[1]);
        },
        error: function(data) {
            $('#article_view_text').html('error');
        }
    });
}

function like_users(e, id, msg) {
    var marginX = 10;
    var marginY = 20;
    var width = 250;
    var top = e.clientY + $(document).scrollTop() + marginY;
    var left = e.clientX - (width - 10) + $(document).scrollLeft();
    if (e.clientX - (width - 10) < marginX)
        left = marginX + $(document).scrollLeft();

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/api/like_users/",
        data: {
            id: id
        },
        success: function(datain) {
            data = "<div style=background:#EDEDED;color:#000;text-align:center;margin-bottom:.5em;padding:.1em>" + msg + "</div>";
            userlist = datain[0].split(',');
            for (user in userlist) {
                data += "<span>" + userlist[user] + "</span> ";
            }
            $('<div/>', {
                id: 'popup_frame',
                class: 'popup_frame',
                html: data,
                style: "width:" + width + "px;position:absolute;top:" + top + "px;left:" + left + "px;"
            }).appendTo('body');
            $('#popup_frame').on('mousedown', function(e) {
                e.stopPropagation();
            })
            $('body').on('mousedown', function(e) {
                $('#popup_frame').remove();
                $('body').off('mousedown');
            })
        },
        error: function(data) {
            $('#article_view_text').html('error');
        }
    });
}
