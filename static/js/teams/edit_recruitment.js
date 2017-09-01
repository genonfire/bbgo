function cacnel() {
    history.back(1);
}

function slot_minus() {
    slot = $('#id_slot_total').val();
    if (slot > 2) {
        $('#id_slot_total').val(slot - 1);
    }
}

$('#id_category').change(function() {
    category = $(this).val();
    switch(category) {
        case '레이드':
            $('#id_slot_total').val(6);
            break;
        case '크루시블':
            $('#id_slot_total').val(4);
            break;
        case '나이트폴':
        case '스트라이크':
        case '퀘스트':
        case '기타':
        default:
            $('#id_slot_total').val(3);
            break;
    }
});

$('#edit_article_form').submit(function(e) {
    subject = $('#id_subject').val();

    if (!subject) {
        e.preventDefault();
        alert(gettext('Please fill the subject.'));
        return;
    }

    $(window).unbind('beforeunload');
});

$(window).bind('beforeunload', function(){
    return gettext('Are you sure to quit editing?');
});
