function like_post(id) {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/api/like_post/",
        data: {
            id: id
        },
        success: function(data) {
            toast(data[1], 500);
            if (data[0] > 0) {
                $('#post_view_like_count').html(data[0]);
            }
            $('#like_bait').hide();
        },
        error: function(data) {
            toast(gettext('Error!'), 500);
        }
    });
}

function delete_post(url) {
    if (confirm(gettext("Are you sure to delete this article?"))) {
        location.href = url;
    }
}

appear({
    init: function init(){
    },
    elements: function elements(){
        return document.getElementsByClassName('post_view_buttons');
    },
    appear: function appear(el){
        var popup = document.getElementById("like_bait");
        popup.classList.toggle("show");
    },
    disappear: function disappear(el){
        var popup = document.getElementById("like_bait");
        popup.classList.toggle("show");
    },
    bounds: 100,
    reappear: true
});
