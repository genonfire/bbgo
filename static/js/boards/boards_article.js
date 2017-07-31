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

function show_popup(e, data, width, marginX, marginY) {
    var top = e.clientY + $(document).scrollTop() + marginY;
    var left = e.clientX - (width - 10) + $(document).scrollLeft();
    if (e.clientX - (width - 10) < marginX)
        left = marginX + $(document).scrollLeft();

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
}

function like_users(e, id) {
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
            msg = gettext("who likes");
            data = "<div style=background:#EDEDED;color:#000;text-align:center;margin-bottom:.5em;padding:.1em>" + msg + "</div>";
            if (datain[0] != '0') {
                userlist = datain[0].split(',');
                for (user in userlist) {
                    data += "<span>" + userlist[user] + "</span> ";
                }
            }
            show_popup(e, data, 250, 10, 20);

        },
        error: function(data) {
            $('#article_view_text').html('error');
        }
    });
}

function share_via(e, text) {
    var url = window.location.href;
    var facebook_url = "http://www.facebook.com/share.php?u=" + url;
    var twitter_url = "https://twitter.com/intent/tweet?text=" + text + "&url=" + url
    var data = '<table width="100%"><tr><td><a href="' + facebook_url + '" target=_blank><img src="/static/icons/facebook16.png">Facebook</td></tr><tr><td><a href="' + twitter_url + '" target="_blank"><img src="/static/icons/twitter16.png">Twitter</a></td></tr></table>';

    show_popup(e, data, 90, 20, 20);
}

function delete_article(url) {
    if (confirm(gettext("Are you sure to delete this article?"))) {
        location.href = url;
    }
}

$(window).bind("blur", function() {
    if ($('#popup_frame').length > 0) {
        $('#popup_frame').remove();
        $('body').off('mousedown');
    }
});
