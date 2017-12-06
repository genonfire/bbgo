function cacnel() {
    history.back(1);
}

function save_as_draft() {
    $('#id_status').val('2temp');
    $('#edit_post_form').submit();
}

function save_override() {
    var status = $('#id_status').val();
    if (status == '2temp') {
        $('#id_status').val('1normal');
    }
}

$('#edit_post_form').submit(function(e) {
    title = $('#id_title').val();
    content = $('#id_content').val();

    if (!title) {
        e.preventDefault();
        alert(gettext('Please fill the subject.'));
        return;
    }
    if (!content || content == "<p><br></p>") {
        e.preventDefault();
        alert(gettext('Please fill the contents.'));
        return;
    }

    $(window).off('beforeunload');
});

$(window).on('beforeunload', function(){
    return gettext('Are you sure to quit editing?');
});
