$(document).ready(function() {
    if (search_type && search_word) {
        if (mark_enabled && search_type != 'category') {
            $('body').mark(search_word);
        }
    }
});
