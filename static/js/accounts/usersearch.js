function dashboard_usersearch() {
    var word = $('#search_word').val();
    if (!word) {
        return;
    }
    else if (word.length < 2) {
        alert(gettext("Please input 2 or more characters."));
    }
    var url = usersearch_url.replace(/bbgo_search_word/, word).replace(/condition/, condition);
    location.href = url;
}

function onKeyPress(e) {
    if (e.keyCode == 13) {
        e.preventDefault();
        dashboard_usersearch();
    }
}

$(document).ready(function() {
    if (search_word) {
        $('#search_word').val(search_word);
        if (mark_enabled) {
            $('body').mark(search_word);
        }
    }
});
