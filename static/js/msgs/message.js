$('#send_msg_form').submit(function(e) {
    text = $('#id_text').val().replace(/\s+$/, '');

    if (!text) {
        e.preventDefault();
        alert(gettext('Please fill the contents.'));
        return;
    }
});

$('#id_text').keyup(function(e) {
    var length = $(this).val().length;
    text_len = length.toString() + ' / ' + msg_text_max.toString();
    if ($('#id_text_len').is("span")) {
        $('#id_text_len').html(text_len);
    }
    else {
        $('#id_text_len').val(text_len);
    }
});
