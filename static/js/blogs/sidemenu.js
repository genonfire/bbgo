function search_post_by_all() {
    var search_word = $('#side_search_word').val();
    if (!search_word) {
        return;
    }
    else if (search_word < 2) {
        alert(gettext("Please input 2 or more characters."));
    }
    var url = url_searchpost.replace(/bb/, search_word);
    location.href = url;
}
