function cacnel() {
    history.back(1);
}

$('#edit_article_form').submit(function(e) {
    url = $('#id_reference').val().replace(/htp:\/\//, '').replace(/http;\/\//, '');
    if (url) {
        if (!/^(https?|http):\/\//.test(url)) {
            $('#id_reference').val("http://" + url);
        }
    }

    subject = $('#id_subject').val();
    content = $('#id_content').val();

    if (!subject) {
        e.preventDefault();
        alert(gettext('Please fill the subject.'));
        return;
    }
    if (!content || content == "<p><br></p>") {
        e.preventDefault();
        alert(gettext('Please fill the contents.'));
        return;
    }

    $(window).unbind('beforeunload');
});

$(window).bind('beforeunload', function(){
    return gettext('Are you sure to quit editing?');
});
