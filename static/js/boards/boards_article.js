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
                    usertag = url_userinfo.replace(/\/bb\//, '\/' + userlist[user] +'\/');
                    data += '<span><a href="' + usertag + '">' + userlist[user] + '</a></span> ';
                }
            }
            show_popup(e, data, 250, 10, 20);

        },
        error: function(data) {
            $('#article_view_text').html('error');
        }
    });
}

function share_via(e, app, id, text) {
    var url = window.location.href;
    var scrap_url = "javascript:scrap('" + app + "', '" + id + "')";
    var scrap_text = gettext('scrap');
    var facebook_url = "http://www.facebook.com/share.php?u=" + url;
    var twitter_url = "https://twitter.com/intent/tweet?text=" + text + "&url=" + url
    var data = '<table width="100%"><tr><td><a href="' + scrap_url + '" target=_blank><img src="/static/icons/scrap16.png">' + scrap_text + '</a>' + '</td></tr><tr><td><a href="' + facebook_url + '" target=_blank><img src="/static/icons/facebook16.png">Facebook</a></td></tr><tr><td><a href="' + twitter_url + '" target="_blank"><img src="/static/icons/twitter16.png">Twitter</a></td></tr></table>';

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
