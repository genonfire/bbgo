function search_post_mobile() {
    var search_word = $('#mobile_search_word').val();
    if (!search_word) {
        return;
    }
    else if (search_word < 2) {
        alert(gettext("Please input 2 or more characters."));
    }
    var url = url_searchpost.replace(/bb/, search_word);
    location.href = url;
}


$(document).ready(function() {
    if (search_type && search_word) {
        if (mark_enabled && search_type != 'category') {
            $('body').mark(search_word);
        }
    }
});
