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