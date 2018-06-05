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
            toast(data[1]), 500;
            if (data[0] > 0) {
                $('#article_view_like_count').html(data[0]);
            }
        },
        error: function(data) {
            toast(gettext("Error!"));
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
            toast(data[1], 500);
        },
        error: function(data) {
            toast(gettext("Error!"));
        }
    });
}

function like_users(e, id) {
    var top = e.clientY + $(document).scrollTop()
    var left = e.clientX - 270 + $(document).scrollLeft();
    if (e.clientX < 280)
        left = 10 + $(document).scrollLeft();

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
        success: function(data) {
            $('#like_users_popup').html(data);
            $('#like_users_popup').css({top: top, left: left});
            $('#like_users_popup').show();
            $('#like_users_popup').on('mouseup touchend', function(e) {
                e.stopPropagation();
            })
            $('body').on('mouseup touchend', function(e) {
                $('#like_users_popup').hide();
                $('body').off('mouseup touchend');
            })
        },
        error: function(data) {
            toast(gettext("Error!"));
        }
    });
}

function share_via(e, app, id, text) {
    var url = window.location.href;
    var scrap_url = "javascript:scrap('" + app + "', '" + id + "')";
    var scrap_text = gettext('scrap');
    var facebook_url = "https://www.facebook.com/sharer/sharer.php?u=" + url;
    var twitter_url = "https://twitter.com/intent/tweet?text=" + text + "&url=" + url
    var data = '<table width="100%"><tr><td><a href="' + scrap_url + '" target=_blank><img src="/static/icons/scrap16.png">' + scrap_text + '</a>' + '</td></tr><tr><td><a href="' + facebook_url + '" target=_blank><img src="/static/icons/facebook16.png">Facebook</a></td></tr><tr><td><a href="' + twitter_url + '" target="_blank"><img src="/static/icons/twitter16.png">Twitter</a></td></tr></table>';

    show_popup(e, data, 90, 20, 20);
}

function delete_article(url) {
    if (confirm(gettext("Are you sure to delete this article?"))) {
        location.href = url;
    }
}

$(window).on("blur", function() {
    if ($('#popup_frame').length > 0) {
        $('#popup_frame').remove();
        $('body').off('mouseup touchend');
    }
});
