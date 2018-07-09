function search_inbox() {
    var type = $('#search_type').val();
    var word = $('#search_word').val();
    if (!word) {
        return;
    }
    else if (word.length < 2) {
        alert(gettext("Please input 2 or more characters."));
    }
    var url = search_inbox_url.replace(/type/, type).replace(/word/, word);
    location.href = url;
}

function onKeyPress(e) {
    if (e.keyCode == 13) {
        e.preventDefault();
        search_inbox();
    }
}

$(document).ready(function() {
    if (search_type) {
        $('#search_type').val(search_type);
    }
    if (search_word) {
        $('#search_word').val(search_word);
        if (mark_enabled) {
            $('body').mark(search_word);
        }
    }
    $(".tdlink").click(function() {
        if ($(window).width() < 768) {
            window.location = $(this).data("href");
        }
    });
});
