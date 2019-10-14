function toggle_bookmark(app, id) {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/api/toggle_bookmark/",
        data: {
            app: app,
            id: id
        },
        success: function(datain) {
            $('#header_star').attr("src", datain);
            toast(gettext("Bookmark saved."), 500);
        },
        error: function(data) {
            toast(gettext("Error! Please check bookmarks limitation."));
        }
    });
}

function scrap(app, id) {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/api/scrap/",
        data: {
            app: app,
            id: id
        },
        success: function(datain) {
            if ($('#popup_frame').length > 0) {
                $('#popup_frame').remove();
                $('body').off('mouseup touchend');
            }
            toast(gettext("You've scrapped this article."));
        },
        error: function(data) {
            if ($('#popup_frame').length > 0) {
                $('#popup_frame').remove();
                $('body').off('mouseup touchend');
            }
            toast(gettext("Already scrapped."));
        }
    });
}
